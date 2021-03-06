from django.core.management import call_command
from django.test import override_settings
from tests.utils import get_test_templates

from .utils import ViteTestCase


class TemplatesMixin(object):
    def test_templates(self):
        for template in get_test_templates():
            page = self.browser.new_page()
            url = "{}/tests/vite_test/{}".format(self.live_server_url, template)
            page.goto(url)
            assert page.evaluate("() => window.qunitPassed")
            page.close()


@override_settings(DEBUG=True, ALLOWED_HOSTS=[])
class DevTests(TemplatesMixin, ViteTestCase):
    pass


@override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
class ProdTests(TemplatesMixin, ViteTestCase):
    def setUp(self):
        call_command("collectstatic", clear=True, interactive=False, vite=True)
        super().setUp()
