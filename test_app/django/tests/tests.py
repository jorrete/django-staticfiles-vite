import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from playwright.sync_api import sync_playwright

from django_staticfiles_vite.management.commands.runserver import (
    patch_static_server,
    thread_vite_server,
)


class MyViewTests(StaticLiveServerTestCase):
    @classmethod
    @override_settings(DEBUG=True)
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=False)
        patch_static_server()
        thread_vite_server()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_login(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        # assert len(page.eval_on_selector(".errornote", "el => el.innerText")) > 0
        page.close()
