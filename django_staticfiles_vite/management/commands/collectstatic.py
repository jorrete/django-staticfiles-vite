import os
import shutil
from os.path import exists, join

from django.conf import settings
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import FileSystemFinder, find, get_finders
from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as CollectStaticCommand,
)
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files import File
from django.utils._os import safe_join

from ...settings import VITE_IGNORE_EXCLUDE, VITE_OUT_DIR
from ...utils import (
    clean_path,
    get_bundle_css_name,
    is_path_js,
    normalize_extension,
    path_is_vite_bunlde,
    vite_build,
)


def get_files_patched(storage, ignore_patterns=None, location=""):
    """
    Recursively walk the storage directories yielding the paths
    of all files that should be copied.
    """
    if ignore_patterns is None:
        ignore_patterns = []
    directories, files = storage.listdir(location)
    prefix = getattr(storage, "prefix", None)

    for fn in files:
        # Match only the basename.
        if utils.matches_patterns(fn, ignore_patterns):
            continue

        if prefix and utils.matches_patterns(join(prefix, fn), ignore_patterns):
            continue

        if location:
            fn = os.path.join(location, fn)
            # Match the full file path.
            if utils.matches_patterns(fn, ignore_patterns):
                continue
        yield fn
    for dir in directories:
        if utils.matches_patterns(dir, ignore_patterns):
            continue
        if prefix and utils.matches_patterns(join(prefix, dir), ignore_patterns):
            continue
        if location:
            dir = os.path.join(location, dir)
        yield from get_files_patched(storage, ignore_patterns, dir)


utils.get_files = get_files_patched


class ViteStorage(staticfiles_storage.__class__):
    def post_process(self, *args, **kwargs):
        found_files = args[0]

        for prefixed_path in list(found_files.keys()):
            prefixed_path_clean = normalize_extension(prefixed_path)

            # files already transformed or removed must get out of the manifest
            if not exists(self.path(prefixed_path)):
                del found_files[prefixed_path]

            if path_is_vite_bunlde(prefixed_path_clean):
                found_files[prefixed_path_clean] = (self, prefixed_path_clean)

                if is_path_js(prefixed_path_clean):
                    prefixed_path_css = get_bundle_css_name(
                        normalize_extension(prefixed_path)
                    )
                    if exists(self.path(prefixed_path_css)):
                        found_files[prefixed_path_css] = (self, prefixed_path_css)

        return super().post_process(*args, **kwargs)

    def _open(self, name, mode):
        name = normalize_extension(name)
        path = (
            safe_join(VITE_OUT_DIR, name)
            if path_is_vite_bunlde(name)
            else self.path(name)
        )
        return File(open(path, mode))


class Command(CollectStaticCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = (
            ViteStorage()
            if getattr(staticfiles_storage, "manifest_storage", None)
            else staticfiles_storage
        )

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--vite",
            action="store_true",
            dest="vite",
            help="Serve static files from from Vite",
        )

    def vite_proccess(self):
        self.vite_files = []
        vite_deps = set()
        found_files = {}

        if exists(VITE_OUT_DIR):
            shutil.rmtree(VITE_OUT_DIR)

        for finder in get_finders():
            for path, storage in finder.list(self.ignore_patterns):
                # Prefix the relative path if the source storage contains it
                if getattr(storage, "prefix", None):
                    prefixed_path = join(storage.prefix, path)
                else:
                    prefixed_path = path

                if prefixed_path not in found_files:
                    found_files[prefixed_path] = (path, find(prefixed_path))

                    if path_is_vite_bunlde(path):
                        self.log("Vite building '%s'" % prefixed_path, level=1)
                        deps = vite_build(prefixed_path, find(prefixed_path))
                        for dep in deps:
                            vite_deps.add(dep)

        for prefixed_path, (path, filepath) in found_files.items():
            filepath = clean_path(filepath)
            if (
                filepath in vite_deps
                and not path_is_vite_bunlde(prefixed_path)
                and prefixed_path not in VITE_IGNORE_EXCLUDE
            ):
                self.vite_files.append(prefixed_path)

    def copy_file(self, path, prefixed_path, source_storage):
        if path_is_vite_bunlde(path):
            prefixed_path = normalize_extension(prefixed_path)
            bundle_path = join(VITE_OUT_DIR, prefixed_path)
            dest_path = self.storage.path(prefixed_path)
            shutil.copy(bundle_path, dest_path)

            if is_path_js(prefixed_path):
                bundle_path_css = get_bundle_css_name(bundle_path)
                dest_path_css = get_bundle_css_name(dest_path)
                if exists(bundle_path_css):
                    shutil.copy(bundle_path_css, dest_path_css)
        else:
            # this means that a non native extension that is not being imported
            # has been collected so ignore it
            if prefixed_path != normalize_extension(prefixed_path):
                return
            super().copy_file(path, prefixed_path, source_storage)

    def handle(self, **options):
        self.set_options(**options)
        use_vite = options["vite"]

        if use_vite:
            self.vite_proccess()
            options["ignore_patterns"].extend(self.vite_files)

        super().handle(**options)
