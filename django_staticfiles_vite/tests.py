from time import sleep

from django.contrib.staticfiles.testing import LiveServerTestCase

from .management.commands.runserver import (
    patch_storage,
    restore_storage,
    thread_vite_server,
)
from .utils import kill_vite_server


class ViteLiveServerTestCase(LiveServerTestCase):
    def setUp(self):
        patch_storage()
        thread_vite_server()
        sleep(1)

    def tearDown(self):
        kill_vite_server()
        restore_storage()
