from unittest import skip


from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_list_items(self):
        ...
        self.fail('write me!')
