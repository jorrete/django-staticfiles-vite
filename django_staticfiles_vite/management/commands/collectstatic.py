import shutil
from os.path import exists, join

from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder, find, get_finders
from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as CollectStaticCommand,
)
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files import File
from django.utils._os import safe_join

from ...settings import VITE_OUT_DIR
from ...utils import (
    get_bundle_css_name,
    is_path_js,
    path_is_vite_bunlde,
    vite_build,
    clean_bundle_name,
)


class ViteStorage(staticfiles_storage.__class__):
    def post_process(self, *args, **kwargs):
        found_files = args[0]

        for path in list(found_files.keys()):
            if path_is_vite_bunlde(path):
                filepath = found_files[path][1]
                found_files[path] = (self, filepath)

                if is_path_js(path):
                    path_css = get_bundle_css_name(path)
                    filepath_css = get_bundle_css_name(filepath)
                    print(path_css, filepath_css)
                    if exists(self.path(filepath_css)):
                        found_files[path_css] = (self, filepath_css)

        return super().post_process(*args, **kwargs)

    def _open(self, name, mode):
        path = (
            safe_join(VITE_OUT_DIR, name)
            if path_is_vite_bunlde(name)
            else self.path(name)
        )
        return File(open(path, mode))


class Command(CollectStaticCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = ViteStorage()

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--vite",
            action="store_true",
            dest="vite",
            help="Serve static files from from Vite",
        )

    def vite_proccess(self):
        self.vite_files = {}
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
                    found_files[prefixed_path] = (path, find(path))

                    if path_is_vite_bunlde(path):
                        deps = vite_build(prefixed_path)

                        for dep in deps:
                            vite_deps.add(dep)

        for prefixed_path, (path, filepath) in found_files.items():
            if filepath in vite_deps and not path_is_vite_bunlde(prefixed_path):
                self.vite_files[prefixed_path] = (path, filepath)

    def copy_file(self, path, prefixed_path, source_storage):
        if path_is_vite_bunlde(path):
            bundle_path = join(VITE_OUT_DIR, prefixed_path)
            dest_path = self.storage.path(prefixed_path)
            shutil.copy(bundle_path, dest_path)

            if is_path_js(prefixed_path):
                bundle_path_css = get_bundle_css_name(bundle_path)
                dest_path_css = get_bundle_css_name(dest_path)
                if exists(bundle_path_css):
                    shutil.copy(bundle_path_css, dest_path_css)
        else:
            super().copy_file(path, prefixed_path, source_storage)

    def handle(self, **options):
        self.set_options(**options)
        use_vite = options["vite"]

        if use_vite:
            self.vite_proccess()
            options["ignore_patterns"].extend(self.vite_files.keys())

        super().handle(**options)
