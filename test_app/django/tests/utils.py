import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright

from django_staticfiles_vite.management.commands.runserver import (
    patch_static_server,
    thread_vite_server,
)
from django_staticfiles_vite.utils import kill_vite_server


class ViteTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=False)
        patch_static_server()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        thread_vite_server()

    def tearDown(self):
        kill_vite_server()
