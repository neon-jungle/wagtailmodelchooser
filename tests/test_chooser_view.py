from django.test import TestCase
from django.urls import reverse
from wagtail.core.models import Page
from wagtail.tests.utils import WagtailTestUtils

from tests.app.models import Author, DefaultManagerAuthor


class TestAdminFormSearchable(WagtailTestUtils, TestCase):
    chooser_url = reverse('model_chooser', kwargs={
        'app_label': Author._meta.app_label,
        'model_name': Author._meta.model_name
    })

    def setUp(self):
        super(TestAdminFormSearchable, self).setUp()

        self.login()
        self.home_page = Page.objects.get(pk=2)

        self.ann = Author.objects.create(name='Ann Leckie')
        self.iain = Author.objects.create(name='Iain M. Banks')
        self.ursula = Author.objects.create(name='Ursula K. Le Guin')
        self.terry = Author.objects.create(name='Terry Pratchett')

    def test_chooser_view(self):
        response = self.client.get(self.chooser_url)
        for author in Author.objects.all():
            self.assertContains(response, author.name)

    def test_chooser_search(self):
        response = self.client.get(self.chooser_url, {'q': 'le'})
        self.assertContains(response, self.ann.name)
        self.assertContains(response, self.ursula.name)
        self.assertNotContains(response, self.iain.name)
        self.assertNotContains(response, self.terry.name)


class TestAdminFormBackend(WagtailTestUtils, TestCase):
    chooser_url = reverse('model_chooser', kwargs={
        'app_label': DefaultManagerAuthor._meta.app_label,
        'model_name': DefaultManagerAuthor._meta.model_name
    })

    def setUp(self):
        super(TestAdminFormBackend, self).setUp()

        self.login()
        self.home_page = Page.objects.get(pk=2)

        self.ann = DefaultManagerAuthor.objects.create(name='Ann Leckie')
        self.iain = DefaultManagerAuthor.objects.create(name='Iain M. Banks')
        self.ursula = DefaultManagerAuthor.objects.create(
            name='Ursula K. Le Guin'
        )
        self.terry = DefaultManagerAuthor.objects.create(name='Terry Pratchett')

    def test_chooser_view(self):
        response = self.client.get(self.chooser_url)
        for author in Author.objects.all():
            self.assertContains(response, author.name)

    def test_chooser_search_backend(self):
        response = self.client.get(self.chooser_url, {'q': 'le'})
        self.assertContains(response, self.ann.name)
        self.assertContains(response, self.ursula.name)
        self.assertNotContains(response, self.iain.name)
        self.assertNotContains(response, self.terry.name)
