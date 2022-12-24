from ..selenium import SeleniumTestCase
from . import QUnitTestCase


class QUitSeleniumTestCase(
    QUnitTestCase,
    SeleniumTestCase,
):
    @classmethod
    def isHeadless(cls):
        return not cls.isDebug()

    def load_qunit_url(self, url):
        self.selenium.get(f"{self.live_server_url}{url}")

    def get_qunit_result(self):
        qunit = self.selenium.execute_async_script(
            """
         window.qunitDone(arguments[0])
        """
        )
        return qunit["failed"] == 0
