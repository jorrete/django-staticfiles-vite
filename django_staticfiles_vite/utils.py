import multiprocessing
import os
import signal
import subprocess
import sys
from json import dumps, loads
from os.path import splitext

import psutil
from django.apps import apps
from django.conf import settings

from .settings import (
    CSS_EXTENSIONS,
    JS_EXTENSIONS,
    VITE_BUNDLE_KEYWORD,
    VITE_EXTENSION_MAP,
    VITE_OUT_DIR,
    VITE_PORT,
    VITE_ROOT,
    VITE_TSCONFIG_GENERATE,
    VITE_TSCONFIG_PATH,
    VITE_URL,
)

TESTING = sys.argv[1:2] == ["test"]


def path_is_vite_bunlde(name):
    return ".{}".format(VITE_BUNDLE_KEYWORD) in name


def clean_bundle_name(name):
    base, extension = splitext(name)
    new_extension = extension

    for target in VITE_EXTENSION_MAP.keys():
        if extension in VITE_EXTENSION_MAP.get(target):
            new_extension = target

    return "{}{}".format(base, new_extension)


def get_bundle_css_name(path):
    return path.replace(".js", ".js.css")


def write_tsconfig(paths):
    with open(VITE_TSCONFIG_PATH, "w") as file:
        file.write(
            dumps(
                {
                    "compilerOptions": {
                        "include": ["{}/**/*".format(path) for path in paths],
                        "paths": {"/static/*": ["{}/*".format(path) for path in paths]},
                    }
                }
            )
        )


def thread_vite_server():
    vite_process = multiprocessing.Process(target=vite_serve)
    vite_process.start()


def kill_vite_server():
    for proc in psutil.process_iter():
        cmd = proc.cmdline()
        path = cmd[1] if len(cmd) > 1 else None
        args = cmd[2] if len(cmd) > 2 else None
        try:
            if path and path.endswith("django-vite-serve") and str(VITE_PORT) in args:
                os.kill(proc.pid, signal.SIGTERM)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def vite_serve():
    paths = apps.get_app_config("django_staticfiles_vite").paths
    arguments = dumps(
        {
            "base": VITE_URL,
            "cssExtensions": CSS_EXTENSIONS,
            "jsExtensions": JS_EXTENSIONS,
            "paths": paths if settings.DEBUG else [str(settings.STATIC_ROOT)],
            "port": VITE_PORT,
            "root": VITE_ROOT if settings.DEBUG else str(settings.STATIC_ROOT),
        }
    )

    if VITE_TSCONFIG_GENERATE:
        write_tsconfig(paths)

    env = os.environ.copy()

    # Can't remeber why here use subprocess and os.system in others
    # maybe because it's a live command
    subprocess.run(
        args=[
            "npx",
            "django-vite-serve",
            "{}".format(arguments),
        ],
        cwd=settings.ROOT_DIR,
        env=env,
        encoding="utf8",
        capture_output=TESTING,
    )


def vite_build(name):
    paths = apps.get_app_config("django_staticfiles_vite").paths
    base, extension = splitext(clean_bundle_name(name))
    filename = "{}{}".format(base, extension)
    arguments = dumps(
        {
            "base": VITE_URL,
            "cssExtensions": CSS_EXTENSIONS,
            "jsExtensions": JS_EXTENSIONS,
            "filename": filename,
            "format": "iife",
            "name": base,
            "outDir": VITE_OUT_DIR,
            "paths": paths,
        }
    )

    env = os.environ.copy()

    pipe = subprocess.run(
        args=[
            "npx",
            "django-vite-build",
            "{}".format(arguments),
        ],
        cwd=settings.ROOT_DIR,
        env=env,
        encoding="utf8",
        stdout=subprocess.PIPE,
    )

    return loads(pipe.stdout.split("\n")[-1])


def is_path_js(path):
    _, extension = splitext(path)
    return extension in JS_EXTENSIONS
