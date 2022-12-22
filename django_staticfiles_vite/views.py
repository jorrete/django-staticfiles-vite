import glob
import inspect
from importlib import import_module
from os.path import join, splitext

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, Template
from django.utils.module_loading import import_string

from .tests.qunit import QUnitTestCase


def get_test_module(test_path):
    return import_module(
        splitext(test_path)[0].replace(str(settings.BASE_DIR), "")[1:].replace("/", ".")
    )


def get_qunit_tests_from_module(mod):
    return [
        obj
        for name, obj in inspect.getmembers(mod)
        if (
            inspect.isclass(obj)
            and mod.__name__ == obj.__module__
            and issubclass(obj, QUnitTestCase)
        )
    ]


def get_test_files():
    test_path = join(settings.BASE_DIR, "*/tests/**/test_*.py")
    return glob.glob(test_path, recursive=True)


def get_tests():
    test_files = get_test_files()
    test_modules = [get_test_module(test_path) for test_path in test_files]
    test_classes = [
        test_class
        for test_module in test_modules
        for test_class in get_qunit_tests_from_module(test_module)
    ]
    return test_classes


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
