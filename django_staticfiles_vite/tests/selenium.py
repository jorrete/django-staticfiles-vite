from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


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
