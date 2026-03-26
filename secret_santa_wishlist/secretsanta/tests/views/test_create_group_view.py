"""Tests for CreateGroupView."""

from pyexpat.errors import messages
from django.test import TestCase
from django.urls import reverse
from secretsanta.forms.create_group_form import CreateGroupForm
from secretsanta.models import User, Group, GroupMember
from secretsanta.tests.helpers import LogInTester

class CreateGroupViewTestCase(TestCase, LogInTester):
    """Tests of the create group view."""

    fixtures = ['secretsanta/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('create_group')
        self.user = User.objects.get(username='johndoe')

    # test create group url
    def test_create_group_url(self):
        self.assertEqual(self.url, '/create_group/')

    # test redirect if not logged in
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('log_in') + '?next=' + self.url)

    # test successful create family group
    def test_successful_create_family_group(self):
        self.client.login(username='johndoe', password='Password123')
        form_input = { 'name': 'Family Test Group', 'group_type': 'family' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 302)
        group = Group.objects.get(name='Family Test Group')
        self.assertEqual(group.group_type, 'family')
        self.assertEqual(group.admin, self.user)
        group_member = GroupMember.objects.get(user=self.user, group=group)
        self.assertTrue(group_member.is_admin)

    # test successful create work group
    def test_successful_create_work_group(self):
        self.client.login(username='johndoe', password='Password123')
        form_input = { 'name': 'Work Test Group', 'group_type': 'work' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 302)
        group = Group.objects.get(name='Work Test Group')
        self.assertEqual(group.group_type, 'work')
        self.assertEqual(group.admin, self.user)
        group_member = GroupMember.objects.get(user=self.user, group=group)
        self.assertTrue(group_member.is_admin)  

    # test successful create friends group
    def test_successful_create_friends_group(self):
        self.client.login(username='johndoe', password='Password123')
        form_input = { 'name': 'Friends Test Group', 'group_type': 'friends' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 302)
        group = Group.objects.get(name='Friends Test Group')
        self.assertEqual(group.group_type, 'friends')
        self.assertEqual(group.admin, self.user)
        group_member = GroupMember.objects.get(user=self.user, group=group)
        self.assertTrue(group_member.is_admin)    

    # test unsuccessful create group with blank name
    def test_unsuccessful_create_group_blank_name(self):
        self.client.login(username='johndoe', password='Password123')
        form_input = { 'name': '', 'group_type': 'family' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_group.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateGroupForm))
        self.assertTrue(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)    
        self.assertIn('name', form.errors)   

    #    

