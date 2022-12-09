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


def build_prefix_path(path):
    return "{}/{}".format(path[1], path[0]) if path[0] else path[1]


def write_tsconfig(paths):
    ts_paths = {}

    for alias, path in paths:
        if alias:
            ts_paths["{}{}/*".format(settings.STATIC_URL, alias)] = [
                "{}/*".format(path)
            ]
            ts_paths["static@{}/*".format(alias)] = ["{}/*".format(path)]
    for alias, path in paths:
        if not alias:
            if "{}*".format(settings.STATIC_URL) not in ts_paths:
                ts_paths["{}*".format(settings.STATIC_URL)] = []
            ts_paths["{}*".format(settings.STATIC_URL)].append("{}/*".format(path))

            if "static@*" not in ts_paths:
                ts_paths["static@*"] = []
            ts_paths["static@*"].append("{}/*".format(path))

    with open(VITE_TSCONFIG_PATH, "w") as file:
        file.write(
            dumps(
                {
                    "compilerOptions": {
                        "include": ["{}/**/*".format(path[1]) for path in paths],
                        "paths": ts_paths,
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
            "paths": paths if settings.DEBUG else [str(settings.STATIC_ROOT)],
            "port": VITE_PORT,
        }
    )

    if VITE_TSCONFIG_GENERATE:
        write_tsconfig(paths)

    env = os.environ.copy()

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


def vite_build(name, filename):
    paths = apps.get_app_config("django_staticfiles_vite").paths
    base, _ = splitext(name)
    arguments = dumps(
        {
            "base": VITE_URL,
            "entry": filename,
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


def clean_path(path):
    return path.replace("lib64", "lib")
