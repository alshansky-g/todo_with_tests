from django.utils import html
import lxml.html
from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')

    def test_renders_input_form(self):
        response = self.client.get('/')
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect('form[method=POST]')
        self.assertEqual(form.get('action'), '/lists/new')
        [input] = form.cssselect('input[name=item_text]')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}')
        self.assertTemplateUsed(response, 'list.html')

    def test_renders_input_form(self):
        mylist = List.objects.create()
        response = self.client.get(f'/lists/{mylist.id}')
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect('form[method=POST]')
        self.assertEqual(form.get('action'), f'/lists/{mylist.id}')
        inputs = form.cssselect('input')
        self.assertIn('item_text', [input.get('name') for input in inputs])

    def test_can_save_a_post_request_to_an_existing_list(self):
        """Тест: можно сохранить post-запрос в существующий список."""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}',
            data={'item_text': 'A new item for an existing list'},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_post_redirects_to_list_view(self):
        """Тест: переадресуется в представление списка."""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}',
            data={'item_text': 'A new item for an existing list'},
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Item 1', list=correct_list)
        Item.objects.create(text='Item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='Other list Item 1', list=other_list)
        Item.objects.create(text='Other list Item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')
        self.assertNotContains(response, 'Other list Item 1')
        self.assertNotContains(response, 'Other list Item 2')

    def test_passes_correct_list_to_template(self):
        """Тест: передается правильный шаблон списка."""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}')
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    """Тест нового списка."""

    def test_can_save_a_post_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()

        self.assertRedirects(response, f'/lists/{new_list.id}')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = html.escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
