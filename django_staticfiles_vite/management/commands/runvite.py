from django.core.management.commands.runserver import Command as RunserverCommand

from ...utils import vite_serve


class Command(RunserverCommand):
    def handle(self, *args, **options):
        vite_serve()
