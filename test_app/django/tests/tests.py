from django.test import override_settings
from tests.utils import get_test_templates

from .utils import ViteTestCase


@override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
# @override_settings(DEBUG=True, ALLOWED_HOSTS=[])
class MyViewTests(ViteTestCase):
    def test_templates(self):
        # for template in get_test_templates():
        #     page = self.browser.new_page()
        #     url = "{}/vite_test/{}".format(self.live_server_url, template)
        #     page.goto(url)
        #     assert page.evaluate("() => window.qunitPassed")
        #     page.close()

        # import time

        # time.sleep(1)
        template = "test_import.html"
        page = self.browser.new_page()
        url = "{}/vite_test/{}".format(self.live_server_url, template)
        page.goto(url)
        # time.sleep(300)
        assert page.evaluate("() => window.qunitPassed")
        page.close()
