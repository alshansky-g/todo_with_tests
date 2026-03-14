from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR, ExistingListItemForm, DUPLICATE_ITEM_ERROR
from lists.models import Item, List


class ItemFormTest(TestCase):
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        mylist = List.objects.create()
        form = ItemForm(data={'text': 'yes'})
        self.assertTrue(form.is_valid())
        new_item = form.save(for_list=mylist)
        self.assertEqual(new_item, Item.objects.get())
        self.assertEqual(new_item.text, 'yes')
        self.assertEqual(new_item.list, mylist)


class ExistingListItemFormTest(TestCase):
    def test_form_validation_for_blank_items(self):
        mylist = List.objects.create()
        form = ExistingListItemForm(for_list=mylist, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        mylist = List.objects.create()
        Item.objects.create(list=mylist, text='no twins!')
        form = ExistingListItemForm(for_list=mylist, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        mylist = List.objects.create()
        form = ExistingListItemForm(for_list=mylist, data={'text': 'hi'})
        self.assertTrue(form.is_valid())
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.get())