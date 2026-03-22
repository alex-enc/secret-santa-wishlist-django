""" Tests for Group Model"""

from django.core.exceptions import ValidationError
from django.test import TestCase
from secretsanta.models.user_model import User
from secretsanta.models.group_model import Group

class GroupModelTestCase(TestCase):
    fixtures = ['secretsanta/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe')

    def test_valid_group(self):
        group = Group(
            name = 'Test Group',
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = self.user
        )
        self._assert_group_is_valid(group)

    # test invalid group

    # test group name cannot be blank
    def test_group_name_cannot_be_blank(self):
        group = Group(
            name = '',
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = self.user
        )
        self._assert_group_is_invalid(group)

    # test group name is too long
    def test_group_name_is_too_long(self):
        group = Group(
            name = 'A' * 101, # 101 characters, should be invalid
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = self.user
        )
        self._assert_group_is_invalid(group)

    # test group code is not unique
    def test_group_code_is_not_unique(self):
        group1 = Group(
            name = 'Test Group 1',
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = self.user
        )
        group1.save()

        group2 = Group(
            name = 'Test Group 2',
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = self.user
        )
        self._assert_group_is_invalid(group2)

       # test group code is unique
    def test_group_code_is_unique(self):
        group1 = Group(
            name = 'Test Group 1',
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = self.user
        )
        group1.save()

        group2 = Group(
            name = 'Test Group 2',
            code = 'ASDFGHJK',
            group_type = 'family',
            admin = self.user
        )
        self._assert_group_is_valid(group2)


    # test group type is not chosen from specified choices
    def test_group_type_is_not_chosen_from_specified_choices(self):
        group = Group(
            name = 'Test Group',
            code = 'ABCDEFGH',
            group_type = 'invalid_choice',
            admin = self.user
        )
        self._assert_group_is_invalid(group)

    # test group type is chosen from specified choices
    def test_group_type_is_chosen_from_specified_choices(self):
        group = Group(
            name = 'Test Group',
            code = 'ABCDEFGH',
            group_type = 'family', # valid choice
            admin = self.user
        )
        self._assert_group_is_valid(group)

    # test group admin cannot be blank
    def test_group_admin_cannot_be_blank(self):
        group = Group(
            name = 'Test Group',
            code = 'ABCDEFGH',
            group_type = 'family',
            admin = None
        )
        self._assert_group_is_invalid(group)

    # test group code length cannot be greater than 8 characters
    def test_group_code_length_cannot_be_greater_than_8_characters(self):
        group = Group(
            name = 'Test Group',
            code = 'toolongcode', # 11 characters, should be invalid
            group_type = 'family',
            admin = self.user
        )
        self._assert_group_is_invalid(group)

    def _assert_group_is_valid(self, group):
        try:
            group.full_clean()
        except ValidationError as e:
            self.fail(f'Test group should be valid but raised ValidationError: {e}')

    def _assert_group_is_invalid(self, group):
        with self.assertRaises(ValidationError):
            group.full_clean()  




 