from django.test import override_settings
from tests.utils import get_test_templates

from .utils import ViteTestCase


@override_settings(DEBUG=True)
class MyViewTests(ViteTestCase):
    def test_templates(self):
        for template in get_test_templates():
            page = self.browser.new_page()
            url = "{}/vite_test/{}".format(self.live_server_url, template)
            page.goto(url)
            assert page.evaluate("() => window.qunitPassed")
            page.close()
