from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest
from functional_tests.my_lists_page import MyListsPage

User = get_user_model()


class MyListsTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.create_pre_authenticated_session('a@b.com')

        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        MyListsPage(self).go_to_my_lists_page(email='a@b.com')
        self.browser.find_element(By.LINK_TEXT, 'Reticulate splines').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        self.browser.find_element(By.LINK_TEXT, 'My lists').click()
        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, 'Click cows'))
        self.browser.find_element(By.LINK_TEXT, 'Click cows').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        self.browser.find_element(By.CSS_SELECTOR, '#id_logout').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.find_elements(By.LINK_TEXT, 'My lists'), [])
        )
