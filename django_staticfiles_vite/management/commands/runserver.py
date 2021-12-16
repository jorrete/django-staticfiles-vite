import multiprocessing
import os

from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin
from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)

from ...utils import vite_serve
from ...views import serve_vite


def patch_static_server():
    def serve(self, request):
        return serve_vite(request)

    StaticFilesHandlerMixin.serve = serve


def thread_vite_server():
    if os.environ.get("DJANGO_VITE_RUNNING") != "1":
        vite_process = multiprocessing.Process(target=vite_serve)
        vite_process.start()
    os.environ["DJANGO_VITE_RUNNING"] = "1"


class Command(RunserverCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--vite",
            action="store_true",
            dest="vite",
            help="Serve static files from from Vite",
        )

    def handle(self, *args, **options):
        use_vite = options["vite"]
        if use_vite:
            patch_static_server()
            thread_vite_server()
        super().handle(*args, **options)
