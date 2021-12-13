from django.apps import AppConfig, apps
from django.contrib.staticfiles.finders import get_finders


def get_static_paths():
    paths = []
    for finder in get_finders():
        if getattr(finder, 'apps', None):
            paths.extend([finder.storages[app].location for app in finder.apps])
        elif getattr(finder, 'locations', None):
            paths.extend([str(path[1]) for path in finder.locations])

    return [path.replace('lib64', 'lib') for path in paths]


class StaticfilesViteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_staticfiles_vite'
    paths = []

    def ready(self):
        if not apps.is_installed('django.contrib.staticfiles'):
            raise Exception('[staticfiles_vite] "django.contrib.staticfiles" must be installed')
        self.paths = get_static_paths()
