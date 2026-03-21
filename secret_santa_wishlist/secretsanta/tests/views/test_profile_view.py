""" Tests for ProfileView"""

from django.test import TestCase
from django.urls import reverse
from secretsanta.models import User, Group, GroupMember
from secretsanta.tests.helpers import LogInTester, reverse_with_next   

class ProfileViewTestCase(TestCase, LogInTester):
    """Tests of the profile view."""

    fixtures = ['secretsanta/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('profile')
        self.user = User.objects.get(username='johndoe')

    # test profile url
    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    # test profile loads correctly for logged in user
    def test_get_profile(self):
        self.client.login(username='johndoe', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    # test profile redirects when not logged in
    def test_get_profile_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse_with_next('log_in', self.url))
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)