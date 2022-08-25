import os
import signal
import subprocess
from json import dumps
from os.path import splitext

import psutil
from django.apps import apps
from django.conf import settings

from .settings import (  # VITE_IMPORT_KEYWORD,
    BUILD_PATH,
    CSS_EXTENSIONS,
    JS_EXTENSIONS,
    POSTCSS_PATH,
    SERVE_PATH,
    VITE_BUNDLE_KEYWORD,
    VITE_CONFIG,
    VITE_EXTENSION_MAP,
    VITE_NODE_MODULES,
    VITE_OUT_DIR,
    VITE_PORT,
    VITE_ROOT,
    VITE_URL,
)


def path_is_vite_bunlde(name):
    return ".{}".format(VITE_BUNDLE_KEYWORD) in name


def clean_bundle_name(name):
    base, extension = splitext(name)
    new_extension = extension

    for target in VITE_EXTENSION_MAP.keys():
        if extension in VITE_EXTENSION_MAP.get(target):
            new_extension = target

    # new_base = base.replace('.{}'.format(VITE_BUNDLE_KEYWORD), '')

    return "{}{}".format(base, new_extension)


def path_is_vite_import(name):
    _, extension = splitext(name)

    if ".{}".format("module") in name:
        return True

    # if ".{}".format(VITE_IMPORT_KEYWORD) in name:
    # return True

    for target in VITE_EXTENSION_MAP.keys():
        if extension in VITE_EXTENSION_MAP.get(target):
            return True

    return False


def vite_serve():
    paths = apps.get_app_config("django_staticfiles_vite").paths
    arguments = dumps(
        {
            "baseUrl": settings.STATIC_URL,
            "base": VITE_URL,
            "configPath": VITE_CONFIG,
            "extensions": JS_EXTENSIONS + CSS_EXTENSIONS,
            "nodeModulesPath": VITE_NODE_MODULES,
            "paths": paths if settings.DEBUG else [str(settings.STATIC_ROOT)],
            "port": VITE_PORT,
            "root": VITE_ROOT if settings.DEBUG else str(settings.STATIC_ROOT),
        }
    )
    env = os.environ.copy()
    env["NODE_PATH"] = VITE_NODE_MODULES
    subprocess.run(
        args=[
            "node",
            SERVE_PATH,
            "{}".format(arguments),
        ],
        env=env,
        encoding="utf8",
    )


def kill_vite_server():
    for proc in psutil.process_iter():
        cmd = proc.cmdline()
        path = cmd[1] if len(cmd) > 1 else None
        args = cmd[2] if len(cmd) > 2 else None
        try:
            if SERVE_PATH == path and str(VITE_PORT) in args:
                os.kill(proc.pid, signal.SIGTERM)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def vite_build(name, entry):
    paths = apps.get_app_config("django_staticfiles_vite").paths
    base, extension = splitext(clean_bundle_name(name))
    filename = "{}{}".format(base, extension)
    arguments = dumps(
        {
            "baseUrl": settings.STATIC_URL,
            "configPath": VITE_CONFIG,
            "entry": entry,
            "extensions": JS_EXTENSIONS + CSS_EXTENSIONS,
            "filename": filename,
            "format": "iife",
            "name": base,
            "outDir": VITE_OUT_DIR,
            "paths": paths,
        }
    )
    os.system(
        "NODE_PATH={} node {} '{}'".format(VITE_NODE_MODULES, BUILD_PATH, arguments)
    )
    return filename


def vite_postcss(name, entry):
    paths = apps.get_app_config("django_staticfiles_vite").paths
    base, _ = splitext(clean_bundle_name(name))
    filename = "{}.css".format(base)
    arguments = dumps(
        {
            "baseUrl": settings.STATIC_URL,
            "paths": paths,
            "outDir": VITE_OUT_DIR,
            "entry": entry,
            "filename": filename,
            "configPath": VITE_CONFIG,
        }
    )
    os.system(
        "NODE_PATH={} node {} '{}'".format(VITE_NODE_MODULES, POSTCSS_PATH, arguments)
    )
    return filename


def is_path_css(path):
    _, extension = splitext(path)
    return extension in CSS_EXTENSIONS


def is_static_request_direct(request):
    return (
        is_path_css(request.path)
        # and "import" not in request.path
        and "direct" not in request.path
        and "django" not in request.path
    )


def get_proxy_url(request):
    url = request.build_absolute_uri().replace(str(request.get_port()), str(VITE_PORT))

    # check is doesnt have part of the paths
    # if settings.DEBUG and is_static_request_direct(request):
    if is_static_request_direct(request):
        url = url + "{}direct".format("&" if "?" in url else "?")

    return url
