from time import sleep

from django.contrib.staticfiles.testing import LiveServerTestCase

from .management.commands.runserver import (
    patch_storage,
    restore_storage,
    thread_vite_server,
)
from .utils import kill_vite_server


class ViteLiveServerTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        patch_storage()
        thread_vite_server()
        sleep(1)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        kill_vite_server()
        restore_storage()
