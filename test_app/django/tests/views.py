from django.shortcuts import render
from tests.utils import get_test_templates


def index(request):
    test_templates = get_test_templates()
    return render(request, "base.html", context={"tests": test_templates})


def test(request, test):
    return render(request, test)
