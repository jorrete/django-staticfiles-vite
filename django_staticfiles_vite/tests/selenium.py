from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from . import ViteLiveServerTestCase
from .qunit import QUnitTestCase


class SeleniumTestCase:
    @classmethod
    def isHeadless(cls):
        return True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        if cls.isHeadless():
            chrome_options.add_argument("--headless")
        cls.selenium = webdriver.Chrome(
            ChromeDriverManager().install(),
            chrome_options=chrome_options,
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


class QUitSeleniumTestCase(
    QUnitTestCase,
    SeleniumTestCase,
    ViteLiveServerTestCase,
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
