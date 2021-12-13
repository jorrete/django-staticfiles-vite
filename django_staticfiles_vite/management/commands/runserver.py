import os
from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)
import threading
from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin
from ...views import serve_vite
from ...utils import vite_serve


def patch_static_server():
    original_serve = StaticFilesHandlerMixin.serve

    def serve(self, request):
        return serve_vite(request)

    StaticFilesHandlerMixin.serve = serve


class Command(RunserverCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--vite', action="store_true", dest='vite',
            help='Serve static files from from Vite',
        )

    def handle(self, *args, **options):
        use_vite = options['vite']
        if use_vite:
            patch_static_server()
            if os.environ.get('DJANGO_VITE_RUNNING') != '1':
                self.stdout.write('Wakeup Vite server.')
                threading.Thread(target=vite_serve).start()
            os.environ['DJANGO_VITE_RUNNING'] = '1'

        super().handle(*args, **options)
