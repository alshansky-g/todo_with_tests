from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        """Тест: нельзя добавлять пустые строки"""
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))

        self.get_item_input_box().send_keys('Купить молоко')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить молоко')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))

        self.get_item_input_box().send_keys('Приготовить чаю')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('2: Приготовить чаю')

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Купить обувь')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить обувь')

        self.get_item_input_box().send_keys('Купить обувь')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, '.invalid-feedback').text,
                "You've already got this in your list",
            )
        )
