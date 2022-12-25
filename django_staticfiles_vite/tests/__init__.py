from time import sleep

from django.core.management import call_command

from ..utils import kill_vite_server, thread_vite_server


def call_collectstatic_vite():
    call_command(
        "collectstatic",
        clear=True,
        tests=True,
        interactive=False,
        verbosity=0,  # no output to keep test clean
        vite=True,
    )


class ViteLiveServerTestCase:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        thread_vite_server()
        sleep(1)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        kill_vite_server()
