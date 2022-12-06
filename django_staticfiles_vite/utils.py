import os
import signal
import multiprocessing
import subprocess
import sys
from json import dumps
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
    VITE_URL,
    VITE_TSCONFIG_GENERATE,
    VITE_TSCONFIG_PATH,
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


def path_is_vite_import(name):
    _, extension = splitext(name)

    if ".{}".format("module") in name:
        return True

    for target in VITE_EXTENSION_MAP.keys():
        if extension in VITE_EXTENSION_MAP.get(target):
            return True

    return False


def write_tsconfig(paths):
    with open(VITE_TSCONFIG_PATH, 'w') as file:
        file.write(dumps({
          "compilerOptions": {
            "include": ["{}/**/*".format(path) for path in paths],
            "paths": {
              "/static/*": ["{}/*".format(path) for path in paths]
            }
          }
        }))


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


def vite_build(name, entry):
    paths = apps.get_app_config("django_staticfiles_vite").paths
    base, extension = splitext(clean_bundle_name(name))
    filename = "{}{}".format(base, extension)
    arguments = dumps(
        {
            "base": VITE_URL,
            "entry": entry,
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

    subprocess.run(
        args=[
            "npx",
            "django-vite-build",
            "{}".format(arguments),
        ],
        cwd=settings.ROOT_DIR,
        env=env,
        encoding="utf8",
        capture_output=TESTING,
    )

    return filename


def vite_postcss(name, entry):
    paths = apps.get_app_config("django_staticfiles_vite").paths
    base, _ = splitext(clean_bundle_name(name))
    filename = "{}.css".format(base)
    arguments = dumps(
        {
            "base": VITE_URL,
            "paths": paths,
            "outDir": VITE_OUT_DIR,
            "entry": entry,
            "filename": filename,
        }
    )

    env = os.environ.copy()

    subprocess.run(
        args=[
            "npx",
            "django-vite-postcss",
            "{}".format(arguments),
        ],
        cwd=settings.ROOT_DIR,
        env=env,
        encoding="utf8",
        capture_output=TESTING,
    )

    return filename


def is_path_css(path):
    _, extension = splitext(path)
    return extension in CSS_EXTENSIONS
