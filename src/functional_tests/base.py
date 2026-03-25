import os
import time
from collections.abc import Callable
from datetime import UTC, datetime
from functools import wraps
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from dotenv import load_dotenv
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox

from functional_tests.container_commands import create_session_on_server, reset_database
from functional_tests.management.commands.create_session import create_pre_authenticated_session

MAX_WAIT = 10
SCREEN_DUMP_LOCATION = Path(__file__).absolute().parent / 'screendumps'
load_dotenv()


def wait(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return func(*args, **kwargs)
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    return wrapper


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = self.firefox
        self.test_server = os.environ.get('TEST_SERVER')
        if self.test_server:
            self.live_server_url = f'http://{self.test_server}'
            reset_database(self.test_server)

    def tearDown(self) -> None:
        if self._test_has_failed():
            if not SCREEN_DUMP_LOCATION.exists():
                SCREEN_DUMP_LOCATION.mkdir(parents=True)
            self.take_screenshot()
            self.dump_html()
        self.browser.quit()
        super().tearDown()

    def create_pre_authenticated_session(self, email: str):
        if self.test_server:
            session_key = create_session_on_server(self.test_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie({
            'name': settings.SESSION_COOKIE_NAME,
            'value': session_key,
            'path': '/',
        })

    def _test_has_failed(self):
        return self._outcome.result.failures or self._outcome.result.errors

    def take_screenshot(self):
        path = SCREEN_DUMP_LOCATION / self._get_filename('png')
        print(f'screenshotting to {path}')
        self.browser.get_screenshot_as_file(str(path))

    def dump_html(self):
        path = SCREEN_DUMP_LOCATION / self._get_filename('html')
        print(f'dumping page html to {path}')
        path.write_text(self.browser.page_source)

    def _get_filename(self, extension: str):
        timestamp = datetime.now(UTC).isoformat().replace(':', '.')[:19]
        return f'{self.__class__.__name__}.{self._testMethodName}-{timestamp}.{extension}'

    def get_item_input_box(self):
        return self.browser.find_element(By.ID, 'id_text')

    def get_page_center(self):
        return self.browser.execute_script('return window.innerWidth') / 2

    @wait
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    @wait
    def wait_for(self, func: Callable):
        return func()

    @wait
    def wait_to_be_logged_in(self, email: str):
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email: str):
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)

    def add_list_item(self, item_text: str):
        num_rows = len(self.browser.find_elements(By.CSS_SELECTOR, '#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text, Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

    @property
    def firefox(self) -> Firefox:
        options = Options()
        options.add_argument('--headless')
        return Firefox(options=options)
