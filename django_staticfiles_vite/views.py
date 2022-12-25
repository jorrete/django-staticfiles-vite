from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, Template
from django.utils.module_loading import import_string

from .utils import get_tests


def qunit_list_view(request):
    return render(
        request,
        "django_staticfiles_vite/qunit_list.html",
        {
            "tests": [
                {
                    "name": test_class.get_test_name(),
                    "qunit": test_class.get_qunit_tests(),
                }
                for test_class in get_tests()
            ],
        },
    )


def render_template(request, template):
    return render(
        request,
        template,
    )


def render_path(request, path):
    file_content = open(path).read()
    template = Template(file_content)
    rendered_template = template.render(
        RequestContext(
            request,
        )
    )
    return HttpResponse(rendered_template)


def qunit_test_view(request):
    test_path = request.GET.get("qunit", None)
    test = import_string(test_path)

    if test.has_html_file():
        return render_path(
            request,
            test.get_html_path(),
        )

    return render_template(
        request,
        test.template,
    )
