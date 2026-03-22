""" Tests for GroupMember model"""

from django.core.exceptions import ValidationError
from django.test import TestCase
from secretsanta.models.user_model import User
from secretsanta.models.group_model import Group
from secretsanta.models.group_member_model import GroupMember

class GroupMemberModelTestCase(TestCase):
    fixtures = ['secretsanta/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe')

    # test valid group member
    def test_valid_group_member(self):
        group = Group(
            name = 'Test Group',
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = self.user
        )
        group.save()

        group_member = GroupMember(
            user = self.user,
            group = group,
            is_admin = False
        )
        self._assert_group_member_is_valid(group_member)
   
    # test group member with no group
    def test_group_member_with_no_group(self):
        group_member = GroupMember(
            user = self.user,
            group = None,
            is_admin = False
        )
        self._assert_group_member_is_invalid(group_member)

    # test group member with no user
    def test_group_member_with_no_user(self):
        group = Group(
            name = 'Test Group',
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = self.user
        )
        group.save()

        group_member = GroupMember(
            user = None,
            group = group,
            is_admin = False
        )
        self._assert_group_member_is_invalid(group_member)

    # test user cannot join same group twice
    def test_user_cannot_join_same_group_twice(self):
        group = Group(
            name = 'Test Group',
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = self.user
        )
        group.save()

        group_member1 = GroupMember(
            user = self.user,
            group = group,
            is_admin = False
        )
        group_member1.save()

        group_member2 = GroupMember(
            user = self.user,
            group = group,
            is_admin = False
        )
        self._assert_group_member_is_invalid(group_member2)
    
    # test is_admin defaults to False
    def test_is_admin_defaults_to_false(self):
        group = Group(
            name = 'Test Group',
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = self.user
        )
        group.save()
        membership = GroupMember.objects.create(
            user=self.user,
            group=group
        )

        self.assertFalse(membership.is_admin)

    # test date_joined is automatically set when a user joins a group
    def test_date_joined_is_automatically_set(self):
        group = Group(
            name = 'Test Group',
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = self.user
        )
        group.save()
        membership = GroupMember.objects.create(
            user=self.user,
            group=group
        )

        self.assertIsNotNone(membership.date_joined)

    def _assert_group_member_is_valid(self, group):
        try:
            group.full_clean()
        except ValidationError as e:
            self.fail(f'Test group member should be valid but raised ValidationError: {e}')

    def _assert_group_member_is_invalid(self, group):
        with self.assertRaises(ValidationError):
            group.full_clean()  


 