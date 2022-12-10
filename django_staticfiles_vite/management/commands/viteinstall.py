import json
from pathlib import Path
import subprocess
from os import environ, getcwd
from os.path import dirname, join, expanduser

from django.conf import settings
from django.core.management.commands.runserver import Command as RunserverCommand

import django_staticfiles_vite

from ...utils import vite_serve, get_pgk_json

VITE_DEPENDENCIES = [
    "vite@^3.2.4",
    "postcss-replace@^2.0.0",
]


def run_command(command):
    env = environ.copy()

    subprocess.run(
        args=command,
        cwd=settings.ROOT_DIR,
        env=env,
        encoding="utf8",
    )

class Command(RunserverCommand):
    def handle(self, *args, **options):
        pkg_path = get_pgk_json(getcwd())
        if not pkg_path.is_file():
            run_command(
                [
                    "npm",
                    "init",
                    "--yes",
                ]
            )
        run_command(
            [
                "npm",
                "install",
            ] + VITE_DEPENDENCIES
        )
