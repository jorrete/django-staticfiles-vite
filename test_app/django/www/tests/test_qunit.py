from django.contrib.staticfiles import testing
from django.test import override_settings

from django_staticfiles_vite import tests
from django_staticfiles_vite.tests import call_collectstatic_vite
from django_staticfiles_vite.tests.qunit import live, playwright, selenium


@override_settings(DEBUG=True, ALLOWED_HOSTS=[])
class PlayStandalineTestCase(
    live.QUnitLiveServerTestCase,
    playwright.QUitPlaywrightTestCase,
    tests.ViteLiveServerTestCase,
    testing.LiveServerTestCase,
):
    qunit_file_paths = [
        "/www/tests/test_qunit.js",
    ]


@override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
class PlayStandalineDeployTestCase(
    live.QUnitLiveServerTestCase,
    playwright.QUitPlaywrightTestCase,
    tests.ViteLiveServerTestCase,
    testing.LiveServerTestCase,
):
    qunit_file_paths = [
        "/www/tests/test_qunit.js",
    ]

    @classmethod
    def setUpClass(cls):
        call_collectstatic_vite()
        super().setUpClass()


@override_settings(DEBUG=True, ALLOWED_HOSTS=[])
class PlayURLTestCase(
    live.QUnitLiveServerTestCase,
    playwright.QUitPlaywrightTestCase,
    tests.ViteLiveServerTestCase,
    testing.LiveServerTestCase,
):
    url = "/"


@override_settings(DEBUG=True, ALLOWED_HOSTS=[])
class SeleniumFooTestCase(
    live.QUnitLiveServerTestCase,
    selenium.QUitSeleniumTestCase,
    tests.ViteLiveServerTestCase,
    testing.LiveServerTestCase,
):
    pass
