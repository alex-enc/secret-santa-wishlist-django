""" Tests for NewGroupInfoView """

from django.test import TestCase
from django.urls import reverse
from secretsanta.models import User, Group, GroupMember
from secretsanta.tests.helpers import LogInTester, reverse_with_next   

class NewGroupInfoViewTestCase(TestCase, LogInTester):
    """Tests of the new group info view."""

    fixtures = ['secretsanta/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('new_group_info')
        self.user = User.objects.get(username='johndoe')

    # test new group info url
    def test_new_group_info_url(self):
        self.assertEqual(self.url, '/new_group_info/')

    # test new group info loads correctly for not logged in user
    def test_get_new_group_info(self):
        self.client.login(username='johndoe', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_group_info.html')

    # test new group info redirects when logged in
    def test_get_new_group_info_redirects_when_logged_in(self):
        self.client.login(username='johndoe', password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # test new group info redirects when not logged in
    def test_get_new_group_info_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse_with_next('log_in', self.url))
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    