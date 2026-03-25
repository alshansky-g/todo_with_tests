from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox

from functional_tests.base import FunctionalTest


def quit_if_possible(browser: Firefox):
    try:
        browser.quit()
    except Exception:
        pass


class SharingTest(FunctionalTest):
    def test_can_share_a_list_with_another_user(self):
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        oni_browser = self.firefox
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('onesiphorus@example.com')

        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Get help')

        share_box = self.browser.find_element(
            By.CSS_SELECTOR, 'input[name="sharee"]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )
