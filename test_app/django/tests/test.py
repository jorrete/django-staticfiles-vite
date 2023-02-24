# from django.contrib.staticfiles.testing import LiveServerTestCase
# from django.test import override_settings
# from tests.utils import get_test_templates
#
# from django_staticfiles_vite.tests import (
#     ViteLiveServerTestCase,
#     call_collectstatic_vite,
# )
#
# from .utils import PlaywrightTestCase
#
#
# class TemplatesMixin(object):
#     def test_templates(self):
#         for template in get_test_templates():
#             page = self.browser.new_page()
#             url = f"{self.live_server_url}/tests/vite_test/{template}"
#             page.goto(url)
#             assert page.evaluate("() => window.qunitPassed")
#             page.close()


# @override_settings(DEBUG=True, ALLOWED_HOSTS=[])
# class DevTests(TemplatesMixin, PlaywrightTestCase, ViteLiveServerTestCase):
#     def setUp(self):
#         super().setUp()


# @override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
# class ProdTests(TemplatesMixin, PlaywrightTestCase, LiveServerTestCase):
#     def setUp(self):
#         call_collectstatic_vite()
#         super().setUp()
