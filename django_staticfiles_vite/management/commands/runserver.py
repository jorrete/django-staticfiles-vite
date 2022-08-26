import multiprocessing
import os

from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin
from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)

from ...utils import vite_serve
from ...views import serve_vite


def patch_static_server(handler=StaticFilesHandlerMixin):
    _serve = handler.serve

    def serve(self, request):
        response = serve_vite(request)
        if response.status_code == 404:
            return _serve(self, request)
        return response

    handler.serve = serve


def thread_vite_server():
    vite_process = multiprocessing.Process(target=vite_serve)
    vite_process.start()


class Command(RunserverCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--vite",
            nargs="?",
            type=str,
            dest="vite",
            help="Serve static files from from Vite",
        )

    def handle(self, *args, **options):
        use_vite = options["vite"]
        if use_vite in ["auto", "external"]:
            if use_vite == "auto":
                if os.environ.get("DJANGO_VITE_RUNNING") != "1":
                    thread_vite_server()
                os.environ["DJANGO_VITE_RUNNING"] = "1"

        super().handle(*args, **options)

    def get_handler(self, *args, **options):
        handler = super().get_handler(*args, **options)
        patch_static_server(handler.__class__)
        return handler

    def get_application(self, options):
        application = super().get_application(options)
        patch_static_server(application.staticfiles_handler_class)
        return application
