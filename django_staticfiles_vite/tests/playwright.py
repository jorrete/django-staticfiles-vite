from os import environ

from playwright.sync_api import sync_playwright


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
        cls.page = cls.browser.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()
