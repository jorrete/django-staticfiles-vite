import os
from time import sleep

from django.contrib.staticfiles.testing import LiveServerTestCase
from django.template.loader import engines
from playwright.sync_api import sync_playwright

from django_staticfiles_vite.tests import ViteLiveServerTestCase


class PlaywrightTestCase:
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        headless = os.getenv("DJANGO_TEST_HEADLESS", "true") != "false"
        cls.browser = cls.playwright.chromium.launch(headless=headless)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()


def get_template_dirs():
    template_dirs = []
    for engine in engines.all():
        template_dirs.extend([str(path) for path in engine.template_dirs])
    return template_dirs


def get_test_templates():
    templates = []
    for template_dir in get_template_dirs():
        for root, dir, files in os.walk(template_dir):
            for file in files:
                if file.startswith("test_") and file.endswith(".html"):
                    template_name = os.path.join(root, file).replace(template_dir, "")[
                        1:
                    ]
                    if template_name not in templates:
                        templates.append(template_name)
    return templates
