from ..playwright import PlaywrightTestCase
from . import QUnitTestCase


class QUitPlaywrightTestCase(
    QUnitTestCase,
    PlaywrightTestCase,
):
    @classmethod
    def isHeadless(cls):
        return not cls.isDebug()

    def load_qunit_url(self, url):
        self.page.goto(f"{self.live_server_url}{url}")

    def get_qunit_result(self):
        qunit = self.page.evaluate(
            """async () => {
            return new Promise((resolve) => {
                window.qunitDone(resolve);
            });
        }"""
        )
        return qunit["failed"] == 0
