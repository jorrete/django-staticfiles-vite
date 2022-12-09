from django.core.management import call_command
from django.test import override_settings
from tests.utils import get_test_templates

from .utils import ViteLiveServerTestCase, PlaywrightTestCase, LiveServerTestCase
from django_staticfiles_vite.tests import call_collectstatic_vite


class TemplatesMixin(object):
    def test_templates(self):
        for template in get_test_templates():
            page = self.browser.new_page()
            url = "{}/tests/vite_test/{}".format(self.live_server_url, template)
            page.goto(url)
            assert page.evaluate("() => window.qunitPassed")
            page.close()


@override_settings(DEBUG=True, ALLOWED_HOSTS=[])
class DevTests(TemplatesMixin, PlaywrightTestCase, ViteLiveServerTestCase):
    pass


@override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
class ProdTests(TemplatesMixin, PlaywrightTestCase, LiveServerTestCase):
    def setUp(self):
        call_collectstatic_vite()
        super().setUp()
