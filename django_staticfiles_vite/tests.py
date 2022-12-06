from time import sleep

from django.contrib.staticfiles.testing import LiveServerTestCase

from .utils import kill_vite_server, thread_vite_server


class ViteLiveServerTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        thread_vite_server()
        sleep(1)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        kill_vite_server()
