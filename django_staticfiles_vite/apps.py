import glob
from os.path import join

from django.apps import AppConfig, apps
from django.conf import settings
from django.contrib.staticfiles.finders import get_finders

from .utils import clean_path


def get_test_paths():
    test_path = join(settings.BASE_DIR, "*/tests/")
    return [
        ["/".join(path[1:-1].split("/")[-2:]), path[:-1]]
        for path in glob.glob(test_path, recursive=True)
    ]


def get_static_paths():
    paths = []
    for finder in get_finders():
        if getattr(finder, "apps", None):
            paths.extend(
                [["", clean_path(finder.storages[app].location)] for app in finder.apps]
            )
        elif getattr(finder, "locations", None):
            paths.extend(
                [[path[0], clean_path(str(path[1]))] for path in finder.locations]
            )

    return paths


class StaticfilesViteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_staticfiles_vite"
    paths = []

    def ready(self):
        if not apps.is_installed("django.contrib.staticfiles"):
            raise Exception(
                '[staticfiles_vite] "django.contrib.staticfiles" must be installed'
            )
        self.paths = get_static_paths()
        self.test_paths = get_test_paths()
