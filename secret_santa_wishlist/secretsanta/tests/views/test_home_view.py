""" Tests for HomeView  """

from django.test import TestCase
from django.urls import reverse
from secretsanta.models import User, Group, GroupMember
from secretsanta.tests.helpers import LogInTester, reverse_with_next   

class HomeViewTestCase(TestCase, LogInTester):
    """Tests of the home view."""

    fixtures = ['secretsanta/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(username='johndoe')

    # test home url   
    def test_home_url(self):
        self.assertEqual(self.url, '/')

    # test home loads correctly for not logged in user
    def test_get_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    # test home redirects when logged in
    def test_get_home_redirects_when_logged_in(self):
        self.client.login(username='johndoe', password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    
    