""" Tests for DashboardView  """

from pyexpat.errors import messages

from django.test import TestCase
from django.urls import reverse
from secretsanta.models import User, Group, GroupMember, Wishlist, WishlistItem
from secretsanta.tests.helpers import LogInTester, reverse_with_next   

class DashboardViewTestCase(TestCase, LogInTester):
    """Tests of the dashboard view."""

    fixtures = ['secretsanta/tests/fixtures/default_user.json',
                'secretsanta/tests/fixtures/other_user.json',
                'secretsanta/tests/fixtures/default_group.json',
                'secretsanta/tests/fixtures/other_group.json']

    def setUp(self):
        self.url = reverse('dashboard')
        self.user = User.objects.get(username='johndoe')
        self.group = Group.objects.get(code='DEFAULT123')
        self.group2 = Group.objects.get(code='OTHER123')

        self.wishlist = Wishlist.objects.create(
            user=self.user,
            group=self.group
        )

        self.item = WishlistItem.objects.create(
            wishlist=self.wishlist,
            item_name="Test Item"
        )

    # test dashboard url
    def test_dashboard_url(self):
        self.assertEqual(self.url, '/dashboard/')

    # test dashboard loads correctly for logged in user
    def test_get_dashboard(self):
        self.client.login(username=self.user.username   , password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    # test dashboard redirects when not logged in
    def test_get_dashboard_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse_with_next('log_in', self.url))
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # test dashboard contains correct groups
    def test_dashboard_contains_correct_groups(self):
        self.client.login(username=self.user.username, password='Password123')
        group1 = self.group
        group2 = self.group2
        GroupMember.objects.create(user=self.user, group=group1, is_admin=True)
        GroupMember.objects.create(user=self.user, group=group2, is_admin=True)     
        response = self.client.get(self.url)
        groups = response.context['member_groups']
        self.assertIn(group1, groups)
        self.assertIn(group2, groups)
        
    # test available groups show up in dropdown
    def test_available_groups_show_up_in_dropdown(self):
        self.client.login(username=self.user.username, password='Password123')
        group1 = self.group
        group2 = self.group2
        GroupMember.objects.create(user=self.user, group=group1, is_admin=True)
        GroupMember.objects.create(user=self.user, group=group2, is_admin=True)
        response = self.client.get(self.url)
        self.assertContains(response, '<option value="{}"'.format(group1.id))
        self.assertContains(response, '<option value="{}"'.format(group2.id))   


        # test dashboard shows no groups when user belongs to no groups
    def test_dashboard_shows_no_groups_when_user_belongs_to_no_groups(self):
        self.client.login(username='johndoe', password='Password123')
        response = self.client.get(self.url)
        groups = response.context['member_groups']
        self.assertEqual(len(groups), 0)

    # test dashboard shows correct wishlist items for selected group
    def test_dashboard_shows_correct_wishlist_items_for_selected_group(self):
        self.client.login(username=self.user.username, password='Password123')
        user1 = User.objects.get(username='johndoe')
        GroupMember.objects.create(user=user1, group=self.group, is_admin=True)
        response = self.client.get(self.url)

        items = response.context['items']
        self.assertIn(self.item, items)

    # test dashboard does not show incorrect wishlist items for other group
    def test_dashboard_shows_only_correct_wishlist_items(self):
        self.client.login(username=self.user.username, password='Password123')

        # Users
        user1 = User.objects.get(username='johndoe')
        user2 = User.objects.get(username='janedoe')

        # Groups
        group1 = Group.objects.get(code='DEFAULT123')
        group2 = Group.objects.get(code='OTHER123')

        # Memberships
        GroupMember.objects.create(user=user1, group=group1)
        GroupMember.objects.create(user=user1, group=group2)
        GroupMember.objects.create(user=user2, group=group1)

        # Wishlists

        wishlist2 = Wishlist.objects.create(user=user1, group=group2)
        wishlist3 = Wishlist.objects.create(user=user2, group=group1)

        # Items
        item1 = WishlistItem.objects.create(
            wishlist=self.wishlist,
            item_name="Correct Item"
        )

        item2 = WishlistItem.objects.create(
            wishlist=wishlist2,
            item_name="Wrong Group Item"
        )

        item3 = WishlistItem.objects.create(
            wishlist=wishlist3,
            item_name="Other User Item"
        )

        # Force selected group = group1
        session = self.client.session
        session["selected_group_id"] = group1.id
        session.save()

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)

        items = response.context['items']

        self.assertIn(item1, items)

        self.assertNotIn(item2, items)
        self.assertNotIn(item3, items)