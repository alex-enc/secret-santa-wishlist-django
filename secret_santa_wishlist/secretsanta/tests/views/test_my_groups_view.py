""" Test for the my_groups view. """

from urllib import response

from django.test import TestCase
from django.urls import reverse
from secretsanta.models import User, Group, GroupMember
from secretsanta.tests.helpers import LogInTester, reverse_with_next   

class MyGroupsViewTestCase(TestCase, LogInTester):
    """Tests of the my_groups view."""

    fixtures = ['secretsanta/tests/fixtures/default_user.json',
                'secretsanta/tests/fixtures/default_group.json',
                'secretsanta/tests/fixtures/other_group.json']

    def setUp(self):
        self.url = reverse('my_groups')
        self.user = User.objects.get(username='johndoe')
        self.group = Group.objects.get(code='DEFAULT123')
        self.group2 = Group.objects.get(code='OTHER123')

    # test my groups
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse_with_next('log_in', self.url))
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # test my groups shows correct groups for logged in user
    def test_my_groups_shows_correct_groups_for_logged_in_user(self):
        self.client.login(username=self.user.username, password='Password123')
        group1 = self.group
        group2 = self.group2

        GroupMember.objects.create(user=self.user, group=self.group, is_admin=True)
        GroupMember.objects.create(user=self.user, group=self.group2, is_admin=True)

        response = self.client.get(reverse('my_groups'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_groups.html')
        # groups in context should be the groups the user belongs to
        groups = response.context['member_groups']
        self.assertIn(group1, groups)
        self.assertIn(group2, groups)

    # test created groups and member groups in context
    def test_created_groups_and_member_groups_in_context(self):
        self.client.login(username=self.user.username, password='Password123')
        GroupMember.objects.create(user=self.user, group=self.group, is_admin=True)
        GroupMember.objects.create(user=self.user, group=self.group2, is_admin=True)

        response = self.client.get(reverse('my_groups'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_groups.html')
        # created groups in context should be the groups the user created
        created_groups = response.context['created_groups']
        self.assertIn(self.group, created_groups)
        self.assertIn(self.group2, created_groups)
        # member groups in context should be the groups the user belongs to
        member_groups = response.context['member_groups']
        self.assertIn(self.group, member_groups)
        self.assertIn(self.group2, member_groups)   

    # test assigned receiver in context for member groups
    def test_assigned_receiver_in_context_for_member_groups(self):
        self.client.login(username=self.user.username, password='Password123')
        GroupMember.objects.create(user=self.user, group=self.group, is_admin=True)
        GroupMember.objects.create(user=self.user, group=self.group2, is_admin=True)

        response = self.client.get(reverse('my_groups'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_groups.html')
        member_groups = response.context['member_groups']
        for group in member_groups:
            self.assertTrue(hasattr(group, 'assigned_receiver'))