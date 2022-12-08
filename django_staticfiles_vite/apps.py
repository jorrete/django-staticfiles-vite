from django.apps import AppConfig, apps
from django.contrib.staticfiles.finders import get_finders


def clean_path(path):
    return path.replace("lib64", "lib")


def get_static_paths():
    paths = []
    for finder in get_finders():
        if getattr(finder, "apps", None):
            paths.extend([['', clean_path(finder.storages[app].location)] for app in finder.apps])
        elif getattr(finder, "locations", None):
            paths.extend([[path[0], clean_path(str(path[1]))] for path in finder.locations])

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
