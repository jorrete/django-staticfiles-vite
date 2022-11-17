import multiprocessing
import os

from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)
from django.contrib.staticfiles.storage import staticfiles_storage

from ... import settings
from ...utils import vite_serve

_base_url = staticfiles_storage._base_url


def patch_storage():
    staticfiles_storage._base_url = "http://localhost:{}".format(settings.VITE_PORT) + _base_url


def restore_storage():
    """
    Used in tests.
    When monkey patched it keeps patched during dev server and prod server tests.
    """
    # bust @cached_property
    del staticfiles_storage.base_url
    staticfiles_storage._base_url = _base_url


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
            patch_storage()

            if use_vite == "auto":
                if os.environ.get("DJANGO_VITE_RUNNING") != "1":
                    thread_vite_server()
                os.environ["DJANGO_VITE_RUNNING"] = "1"

        super().handle(*args, **options)
