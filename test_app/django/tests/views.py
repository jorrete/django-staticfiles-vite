from django.shortcuts import render
from django.utils.log import DEFAULT_LOGGING
from tests.utils import get_test_templates

DEFAULT_LOGGING["handlers"]["console"]["filters"] = []


def index(request):
    test_templates = get_test_templates()
    return render(request, "base.html", context={"tests": test_templates})


def test(request, test):
    return render(request, test)
