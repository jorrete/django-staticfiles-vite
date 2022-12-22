from os import environ

from playwright.sync_api import sync_playwright

from . import ViteLiveServerTestCase
from .qunit import QUnitTestCase


class PlaywrightTestCase:
    @classmethod
    def isHeadless(cls):
        return True

    @classmethod
    def setUpClass(cls):
        environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=cls.isHeadless())

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()


class QUitPlaywrightTestCase(
    QUnitTestCase,
    PlaywrightTestCase,
    ViteLiveServerTestCase,
):
    @classmethod
    def isHeadless(cls):
        return not cls.isDebug()

    def load_qunit_url(self, url):
        self.page = self.browser.new_page()
        self.page.goto(f"{self.live_server_url}{url}")

    def get_qunit_result(self):
        qunit = self.page.evaluate(
            """async () => {
            return new Promise((resolve) => {
                window.qunitDone(resolve);

            });
        }"""
        )
        return qunit["failed"] == 0
