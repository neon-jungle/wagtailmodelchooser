from django.test import TestCase
from django.urls import reverse
from wagtail.models import Page
from wagtail.test.utils import WagtailTestUtils

from tests.app.models import Author, Book


class TestAdminForm(WagtailTestUtils, TestCase):
    def setUp(self):
        super(TestAdminForm, self).setUp()

        self.login()
        self.home_page = Page.objects.get(pk=2)

        Author.objects.bulk_create(
            [
                Author(name="Ann Leckie"),
                Author(name="Iain M. Banks"),
                Author(name="Ursula K. Le Guin"),
                Author(name="Terry Pratchett"),
            ]
        )

    def test_create_book(self):
        create_url = reverse(
            "wagtailadmin_pages:add",
            args=[Book._meta.app_label, Book._meta.model_name, self.home_page.pk],
        )
        response = self.client.get(create_url)

        author = Author.objects.get(name="Ann Leckie")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose author")
        self.assertContains(response, "Choose another author")
        self.assertNotContains(response, "Clear choice")

        response = self.client.post(
            create_url,
            {
                "title": "Ancillary Justice",
                "slug": "ancillary-justice",
                "author": author.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        book = Book.objects.get()
        self.assertEqual(book.author, author)

    def test_edit_book(self):
        author = Author.objects.get(name="Terry Pratchett")

        book = self.home_page.add_child(
            instance=Book(
                title="Night Watch", author=Author.objects.get(name="Terry Pratchett")
            )
        )

        edit_url = reverse("wagtailadmin_pages:edit", args=[book.pk])

        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose author")
        self.assertContains(response, "Choose another author")
        input = '<input id="id_author" name="author" type="hidden" value="4" required />'.format(
            author.pk
        )
        self.assertContains(response, input, html=True)
