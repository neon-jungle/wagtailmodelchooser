from django.test import TestCase
from django.urls import reverse
from wagtail.tests.utils import WagtailTestUtils
from wagtail.wagtailcore.models import Page

from tests.app.models import Author


class TestAdminForm(WagtailTestUtils, TestCase):
    chooser_url = reverse('model_chooser', kwargs={
        'app_label': Author._meta.app_label,
        'model_name': Author._meta.model_name})

    def setUp(self):
        super(TestAdminForm, self).setUp()

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
