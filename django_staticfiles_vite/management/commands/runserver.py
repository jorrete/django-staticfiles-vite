import os

from django.utils.module_loading import import_string

from ...settings import VITE_RUNSERVER_COMMAND_OVERLOAD
from ...utils import thread_vite_server

RunserverCommand = import_string(VITE_RUNSERVER_COMMAND_OVERLOAD)


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
        os.environ["DJANGO_VITE_RUNNING"] = "0"
