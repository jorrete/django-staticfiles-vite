import multiprocessing
import os
import time

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
    print("Wakeup Vite server.")
    vite_process = multiprocessing.Process(target=vite_serve)
    vite_process.start()


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
            if os.environ.get("DJANGO_VITE_RUNNING") != "1":
                thread_vite_server()
            os.environ["DJANGO_VITE_RUNNING"] = "1"

        super().handle(*args, **options)
