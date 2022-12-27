import time
import urllib
from glob import glob
from inspect import getfile
from os import environ
from os.path import basename, dirname, exists, join, splitext

from django.conf import settings

QUNIT_PATTERN = "test_qunit_*"
TESTING_BROWSER_DEBUG = environ.get("TESTING_BROWSER_DEBUG", "false") == "true"
TESTING_BROWSER_FORCE_OPEN = (
    environ.get("TESTING_BROWSER_FORCE_OPEN", "false") == "true"
)


class QUnitTestCase:
    url = "/qunit/test/"
    template = "django_staticfiles_vite/qunit_default.html"
    qunit_file_paths = []

    @classmethod
    def get_qunit_file_paths(cls):
        if len(cls.qunit_file_paths):
            return cls.qunit_file_paths

        file = getfile(cls)
        dir = dirname(file)
        [base, _] = splitext(basename(file))

        return [
            test_path.replace(str(settings.BASE_DIR), "")
            for test_path in glob(join(dir, f"{base}*.js"), recursive=True)
        ]

    @classmethod
    def get_qunit_tests(cls, port=None):
        return [
            {
                "url": cls.get_qunit_url(cls.get_test_name(), qunit_test, port=port),
                "name": qunit_test,
            }
            for qunit_test in cls.get_qunit_file_paths()
        ]

    @classmethod
    def get_html_path(cls):
        [name, _] = splitext(getfile(cls))
        return f"{name}.html"

    @classmethod
    def has_html_file(cls):
        return exists(cls.get_html_path())

    @classmethod
    def setUpClass(cls):
        environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()

    @classmethod
    def isDebug(cls):
        return TESTING_BROWSER_DEBUG

    @classmethod
    def isForceOpen(cls):
        return TESTING_BROWSER_FORCE_OPEN

    @classmethod
    def get_test_name(cls):
        return f"{cls.__module__}.{cls.__name__}"

    @classmethod
    def get_qunit_url(cls, test_name, qunit_test, port=None):
        qunit_test = urllib.parse.quote(
            f"{qunit_test}?qunit" if settings.DEBUG else f"/tests{qunit_test}"
        )

        url = f"{cls.url}?qunit={test_name}&variant={qunit_test}"

        if port:
            url = f"{url}&port={port}"

        return url

    def get_port(self):
        raise NotImplementedError

    def load_qunit_url(self, url):
        raise NotImplementedError

    def get_qunit_result(self, url):
        raise NotImplementedError

    def run_qunit(self, url):
        """
        run QUnit tests
        """
        self.load_qunit_url(url)
        return self.get_qunit_result()

    def test_qunit(self):
        for test in self.get_qunit_tests(self.get_port()):
            with self.subTest(msg=test["name"]):
                passed = self.run_qunit(test["url"])
                if self.isDebug() and not passed:
                    time.sleep(10000000)
                self.assertTrue(passed, "QUnit without errors")
