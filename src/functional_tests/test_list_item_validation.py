from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        """Тест: нельзя добавлять пустые строки"""
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, '.invalid-feedback').text,
                "You can't have an empty list item",
            )
        )

        self.browser.find_element(By.ID, 'id_new_item').send_keys('Купить молоко')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, '.invalid_feedback').text,
                "You can't have an empty list item",
            )
        )

        self.browser.find_element(By.ID, 'id_new_item').send_keys('Налить чаю')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.Enter)
        self.wait_for_row_in_list_table('2: Налить чаю')
