from django.test import override_settings

from django_staticfiles_vite.tests import playwright, selenium


@override_settings(DEBUG=True, ALLOWED_HOSTS=[])
class PlayStandalineTestCase(playwright.QUitPlaywrightTestCase):
    qunit_file_paths = [
        "/www/tests/test_qunit.js",
    ]


@override_settings(DEBUG=True, ALLOWED_HOSTS=[])
class PlayURLTestCase(playwright.QUitPlaywrightTestCase):
    url = "/"


@override_settings(DEBUG=True, ALLOWED_HOSTS=[])
class SeleniumFooTestCase(selenium.QUitSeleniumTestCase):
    pass
