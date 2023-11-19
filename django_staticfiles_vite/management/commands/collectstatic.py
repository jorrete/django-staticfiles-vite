import os
from glob import glob
from os.path import dirname, exists, join

from django.conf import settings
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import find, get_finders
from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as CollectStaticCommand,
)
from django.contrib.staticfiles.storage import staticfiles_storage

from ...utils import (
    get_bundle_css_name,
    is_path_css,
    is_path_js,
    normalize_extension,
    path_is_vite_bunlde,
    vite_build,
)


def collect_test_files():
    files = {
        join("tests", file.replace(str(settings.BASE_DIR), "")[1:]): file + "?qunit"
        for file in glob(
            join(str(settings.BASE_DIR), "*/tests/**/*.js"), recursive=True
        )
    }
    vite_build(files, False)


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
    # XXX when Django 4.2 remove
    patterns = (
        (
            "*.css",
            (
                r"""(?P<matched>url\(['"]{0,1}\s*(?P<url>.*?)["']{0,1}\))""",
                (
                    r"""(?P<matched>@import\s*["']\s*(?P<url>.*?)["'])""",
                    """@import url("%(url)s")""",
                ),
                (
                    (
                        r"(?m)(?P<matched>)^(/\*#[ \t]"
                        r"(?-i:sourceMappingURL)=(?P<url>.*)[ \t]*\*/)$"
                    ),
                    "/*# sourceMappingURL=%(url)s */",
                ),
            ),
        ),
        (
            "*.js",
            (
                (
                    r"(?m)(?P<matched>)^(//# (?-i:sourceMappingURL)=(?P<url>.*))$",
                    "//# sourceMappingURL=%(url)s",
                ),
                (
                    r"""(?P<matched>["'](?P<url>/static/.*?)["'])""",
                    """\"%(url)s\"""",
                ),
            ),
        ),
    )

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
        parser.add_argument(
            "--tests",
            action="store_true",
            dest="tests",
            help="Process js tests",
        )

    def collect_tests(self):
        self.log("Vite building qunit tests", level=1)

        files = {
            join("tests", file.replace(str(settings.BASE_DIR), "")[1:]): file + "?qunit"
            for file in glob(
                join(str(settings.BASE_DIR), "*/tests/**/*.js"), recursive=True
            )
        }
        vite_build(files, False, out_dir=self.storage.location)

    def vite_process_new(self, group_folders=True):
        groups = {}
        files = {}

        for finder in get_finders():
            for path, storage in finder.list(self.ignore_patterns):
                if not path_is_vite_bunlde(path):
                    continue

                # Prefix the relative path if the source storage contains it
                if getattr(storage, "prefix", None):
                    prefixed_path = join(storage.prefix, path)
                else:
                    prefixed_path = path

                dir = dirname(path) if group_folders else "__all__"

                if dir not in groups:
                    groups[dir] = {
                        "js": {},
                        "css": {},
                    }

                bundle = groups[dir]["css"] if is_path_css(path) else groups[dir]["js"]

                bundle[prefixed_path] = find(prefixed_path)
                files[prefixed_path] = storage

        for group in groups.values():
            if len(group["css"].items()):
                self.log("Vite building css", level=1)
                vite_build(group["css"], True, out_dir=self.storage.location)

            if len(group["js"].items()):
                self.log("Vite building js", level=1)
                vite_build(group["js"], False, out_dir=self.storage.location)

        return files

    def handle(self, **options):
        self.set_options(**options)
        use_vite = options["vite"]
        # use_vite = False
        process_tests = options["tests"]

        if self.clear:
            self.clear_dir("")
        options["clear"] = False

        options["ignore_patterns"].extend([
            "*.vite.*",
            "*vite/*",
        ])

        if use_vite:
            files = self.vite_process_new()

        super().handle(**options)

        hashed_files_initial = self.storage.hashed_files

        if use_vite:
            if self.post_process and hasattr(self.storage, "post_process"):
                processor = self.storage.post_process(files, dry_run=self.dry_run)
                for original_path, processed_path, processed in processor:
                    if isinstance(processed, Exception):
                        self.stderr.write(
                            "Post-processing '%s' failed!" % original_path
                        )
                        # Add a blank line before the traceback, otherwise it's
                        # too easy to miss the relevant part of the error message.
                        self.stderr.write()
                        raise processed
                    if processed:
                        self.log(
                            "Post-processed '%s' as '%s'"
                            % (original_path, processed_path),
                            level=2,
                        )
                        self.post_processed_files.append(original_path)
                    else:
                        self.log("Skipped post-processing '%s'" % original_path)

            hashed_files_vite = self.storage.hashed_files
            self.storage.hashed_files.update(hashed_files_initial)
            self.storage.hashed_files.update(hashed_files_vite)
            self.storage.save_manifest()

            if process_tests:
                self.collect_tests()
