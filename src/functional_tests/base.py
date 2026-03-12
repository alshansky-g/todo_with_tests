import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from dotenv import load_dotenv
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox

MAX_WAIT = 5
load_dotenv()


class FunctionalTest(StaticLiveServerTestCase):
    options = Options()
    options.add_argument('--headless')

    def setUp(self) -> None:
        self.browser = Firefox(options=self.options)
        if test_server := os.environ.get('TEST_SERVER'):
            self.live_server_url = f'http://{test_server}'

    def tearDown(self) -> None:
        self.browser.quit()

    def get_page_center(self):
        return self.browser.execute_script('return window.innerWidth') / 2

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
