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

    @classmethod
    def get_qunit_file_paths(cls):
        file = getfile(cls)
        dir = dirname(file)
        [base, _] = splitext(basename(file))
        return [
            test_path.replace(str(settings.BASE_DIR), "")
            for test_path in glob(join(dir, f"{base}*.js"), recursive=True)
        ]

    @classmethod
    def get_qunit_tests(cls):
        return [
            {
                "url": cls.get_qunit_url(
                    cls.get_test_name(),
                    qunit_test,
                ),
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
    def hasFailed(cls):
        return getattr(cls, "_failed", None)

    @classmethod
    def tearDownClass(cls):
        # will hang the test run so you can inspect and close with ctrl-c
        if (cls.isDebug() and cls.hasFailed()) or cls.isForceOpen():
            return
        super().tearDownClass()

    @classmethod
    def get_test_name(cls):
        return f"{cls.__module__}.{cls.__name__}"

    @classmethod
    def get_qunit_url(cls, test_name, qunit_test):
        return f"{cls.url}?qunit={test_name}&variant={qunit_test}"

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
        try:
            for test in self.get_qunit_tests():
                with self.subTest(msg=test["name"]):
                    passed = self.run_qunit(test["url"])
                    self.assertTrue(passed, "QUnit without errors")
            setattr(self.__class__, "_failed", False)
        except Exception as e:
            setattr(self.__class__, "_failed", True)
            raise e
