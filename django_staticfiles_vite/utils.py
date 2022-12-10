import multiprocessing
import os
import signal
import subprocess
import sys
from json import dumps, loads, load
from os import environ
from os.path import dirname, expanduser, join, splitext
from pathlib import Path

import psutil
from django.apps import apps
from django.conf import settings

from . import node
from .settings import (
    CSS_EXTENSIONS,
    JS_EXTENSIONS,
    VITE_BUNDLE_KEYWORD,
    VITE_EXTENSION_MAP,
    VITE_OUT_DIR,
    VITE_PORT,
    VITE_ROOT,
    VITE_TSCONFIG_PATH,
    VITE_URL,
    VITE_TSCONFIG_EXTENDS,
)

TESTING = sys.argv[1:2] == ["test"]


def path_is_vite_bunlde(name):
    return f".{VITE_BUNDLE_KEYWORD}" in name


def normalize_extension(name):
    base, extension = splitext(name)
    new_extension = extension

    for target in VITE_EXTENSION_MAP.keys():
        if extension in VITE_EXTENSION_MAP.get(target):
            new_extension = target

    return f"{base}{new_extension}"


def get_bundle_css_name(path):
    return path.replace(".js", ".js.css")


def build_prefix_path(path):
    return f"{path[1]}/{path[0]}" if path[0] else path[1]


def write_tsconfig(paths):
    tsconfig = VITE_TSCONFIG_EXTENDS
    tsconfig_include = tsconfig.get("compilerOptions", {}).get("include", [])
    tsconfig_paths = tsconfig.get("compilerOptions", {}).get("paths", {})
    print(tsconfig)

    for _, path in paths:
        tsconfig_include.append(f"{path}/**/*")

    # paths with alias must be forced to be first
    for alias, path in paths:
        if alias:
            tsconfig_paths[f"{settings.STATIC_URL}{alias}/*"] = [f"{path}/*"]
            tsconfig_paths[f"static@{alias}/*"] = [f"{path}/*"]

    for alias, path in paths:
        if not alias:
            if f"{settings.STATIC_URL}*" not in tsconfig_paths:
                tsconfig_paths[f"{settings.STATIC_URL}*"] = []
            tsconfig_paths[f"{settings.STATIC_URL}*"].append(f"{path}/*")

            if "static@*" not in tsconfig_paths:
                tsconfig_paths["static@*"] = []
            tsconfig_paths["static@*"].append(f"{path}/*")

    with open(VITE_TSCONFIG_PATH, "w") as file:
        file.write(
            dumps(
                {
                    "compilerOptions": {
                        "paths": tsconfig_paths,
                    },
                    "include": tsconfig_include,
                },
                indent=4,
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
            if path and path.endswith("django_staticfiles_vite/node/serve.js") and str(VITE_PORT) in args:
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

    if VITE_TSCONFIG_PATH:
        write_tsconfig(paths)

    env = environ.copy()
    pkg_path = get_pgk_json(settings.BASE_DIR)
    env["NODE_PATH"] = join(dirname(pkg_path), "node_modules")
    serve_path = join(dirname(__file__), "node", "serve.js")

    subprocess.run(
        args=[
            "node",
            serve_path,
            f"{arguments}",
        ],
        cwd=settings.ROOT_DIR,
        env=env,
        encoding="utf8",
        capture_output=TESTING,
    )


def vite_build(entry, is_css):
    paths = apps.get_app_config("django_staticfiles_vite").paths
    arguments = dumps(
        {
            "buildCSS": is_css,
            "base": VITE_URL,
            "entry": entry,
            "format": "es",
            "outDir": VITE_OUT_DIR,
            "paths": paths,
        }
    )
    env = environ.copy()
    pkg_path = get_pgk_json(settings.BASE_DIR)
    env["NODE_PATH"] = join(dirname(pkg_path), "node_modules")
    build_path = join(dirname(__file__), "node", "build.js")

    pipe = subprocess.run(
        args=[
            "node",
            build_path,
            f"{arguments}",
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


def is_path_css(path):
    _, extension = splitext(path)
    return extension in CSS_EXTENSIONS


def clean_path(path):
    return path.replace("lib64", "lib")


def find_file_up_tree(name, path, root=None):
    path = Path(path)
    file = path / name

    root = root if root else expanduser("~")

    if Path(root) == path:
        return None

    if not file.is_file():
        return find_file_up_tree(name, path.parent)

    return file


def get_pgk_json(path):
    return find_file_up_tree("package.json", path)


def get_tsconfig(path):
    return find_file_up_tree("tsconfig.json", path)
