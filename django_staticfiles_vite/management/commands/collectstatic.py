from os import rename
from os.path import isfile
from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as CollectStaticCommand,
)
from django.contrib.staticfiles.storage import staticfiles_storage
from ...utils import (
    vite_build,
    path_is_vite_import,
    path_is_vite_bunlde,
    is_path_css,
    vite_postcss,
)


def patch_storage(storage):
    original_post_process = staticfiles_storage.post_process

    def post_process(*args, **kwargs):
        args = list(args)
        args[0] = {
            key: value
            for key, value in args[0].items()
            if not path_is_vite_import(key) and not path_is_vite_bunlde(key)
        }
        return original_post_process(*args, **kwargs)

    staticfiles_storage.post_process = post_process


class Command(CollectStaticCommand):
    vite_files = []
    has_manifest = hasattr(staticfiles_storage, "manifest_name")

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--vite",
            action="store_true",
            dest="vite",
            help="Serve static files from from Vite",
        )

    def set_options(self, **options):
        super().set_options(**options)
        self.use_vite = options["vite"]

    def copy_file(self, path, prefixed_path, source_storage):
        if self.use_vite:
            if path_is_vite_bunlde(prefixed_path):
                self.log("Vite build '%s'" % prefixed_path)
                if is_path_css(prefixed_path):
                    name = vite_postcss(
                        prefixed_path,
                        source_storage.path(prefixed_path),
                    )
                else:
                    name = vite_build(
                        prefixed_path,
                        source_storage.path(prefixed_path),
                    )

                filename = name

                if self.has_manifest:
                    filename = staticfiles_storage.hashed_name(filename)

                self.vite_files.append([name, filename])
            elif path_is_vite_import(prefixed_path):
                self.log("Vite delete import '%s'" % prefixed_path)
                self.delete_file(path, prefixed_path, source_storage)
            else:
                super().copy_file(path, prefixed_path, source_storage)
        else:
            super().copy_file(path, prefixed_path, source_storage)

    def handle(self, **options):
        if self.has_manifest:
            patch_storage(staticfiles_storage)

        super().handle(**options)

        if self.use_vite and self.has_manifest:
            for name, filename in self.vite_files:
                css_name = name.replace("js", "css")
                css_filename = filename.replace("js", "css")
                if not is_path_css(name) and isfile(staticfiles_storage.path(css_name)):
                    staticfiles_storage.hashed_files[css_name] = css_filename
                    rename(
                        staticfiles_storage.path(css_name),
                        staticfiles_storage.path(css_filename),
                    )
                staticfiles_storage.hashed_files[name] = filename
                rename(
                    staticfiles_storage.path(name),
                    staticfiles_storage.path(filename),
                )

            staticfiles_storage.save_manifest()
