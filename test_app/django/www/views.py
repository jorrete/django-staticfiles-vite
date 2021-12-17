from django.shortcuts import render
from django.template.loader import engines


def get_template_dirs():
    """
    Load and return a template for the given name.
    Raise TemplateDoesNotExist if no such template exists.
    """
    for engine in engines.all():
        print(engine, type(engine))
        print(engine.template_dirs)


def index(request):
    get_template_dirs()
    return render(request, "test_import.html")
