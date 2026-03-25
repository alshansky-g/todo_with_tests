from typing import Self

from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


class MyListsPage:
    def __init__(self, test: FunctionalTest) -> None:
        self.test = test

    def go_to_my_lists_page(self, email: str) -> Self:
        self.test.browser.get(self.test.live_server_url)
        self.test.browser.find_element(By.LINK_TEXT, 'My lists').click()
        self.test.wait_for(
            lambda: self.test.assertIn(
                email,
                self.test.browser.find_element(By.TAG_NAME, 'h1').text,
            )
        )
        return self
