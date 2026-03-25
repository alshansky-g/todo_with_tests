from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox

from functional_tests.base import FunctionalTest
from functional_tests.list_page import ListPage
from functional_tests.my_lists_page import MyListsPage


def quit_if_possible(browser: Firefox) -> None:
    try:
        browser.quit()
    except Exception:
        pass


class SharingTest(FunctionalTest):
    def test_can_share_a_list_with_another_user(self) -> None:
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        oni_browser = self.firefox
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('onesiphorus@example.com')

        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Get help')

        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com',
        )
        list_page.share_list_with('onesiphorus@example.com')

        self.browser = oni_browser
        MyListsPage(self).go_to_my_lists_page('onesiphorus@example.com')

        self.browser.find_element(By.LINK_TEXT, 'Get help').click()
        self.wait_for(
            lambda: self.assertEqual(
                list_page.get_list_owner(),
                'edith@example.com',
            )
        )

        list_page.add_list_item('Hi Edith!')

        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Edith!', 2)
