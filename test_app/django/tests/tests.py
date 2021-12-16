import time

from django.test import override_settings

from .utils import ViteTestCase


@override_settings(DEBUG=True)
class MyViewTests(ViteTestCase):
    def test_login(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        # assert len(page.eval_on_selector(".errornote", "el => el.innerText")) > 0
        time.sleep(1000)
        page.close()
