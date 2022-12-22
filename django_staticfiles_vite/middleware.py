import sys

from django.template.loader import get_template

from .tests.qunit import TESTING_BROWSER_DEBUG

TESTING = sys.argv[1:2] == ["test"]


def render_qunit(test_path, request):
    template = get_template("django_staticfiles_vite/qunit_base.html")
    return template.render(
        {
            "vite_client": not TESTING or TESTING_BROWSER_DEBUG,
            "test_path": test_path,
        },
    )


class QUnitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        test_path = request.GET.get("qunit", None)
        variant = request.GET.get("variant", None)
        response = self.get_response(request)
        if test_path and variant:
            content = render_qunit(variant, request)
            response.content = response.content.replace(b"</body>", str.encode(content))

        return response
