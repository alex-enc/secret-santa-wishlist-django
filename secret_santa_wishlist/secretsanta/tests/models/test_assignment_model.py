""" Test for Assignment model"""

from django.core.exceptions import ValidationError
from django.test import TestCase
from secretsanta.models.user_model import User
from secretsanta.models.group_model import Group
from secretsanta.models.group_member_model import GroupMember
from secretsanta.models.assignment_model import Assignment

class AssignmentModelTestCase(TestCase):
    fixtures = ['secretsanta/tests/fixtures/default_user.json', 'secretsanta/tests/fixtures/other_user.json']


    def setUp(self):
        self.user = User.objects.get(username='johndoe')

    # test valid assignment
    def test_valid_assignment(self):
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

        user2 = User.objects.get(username='janedoe')
        group_member2 = GroupMember(
            user = user2,
            group = group,
            is_admin = False
        )
        group_member2.save()
        assignment = Assignment(
            group = group,
            giver = group_member1.user,
            receiver = group_member2.user,
            year = 2025

        )   
        self._assert_assignment_is_valid(assignment)

    #  test user cannot be assigned to more than one person in the same year and group
    def test_user_cannot_be_assigned_to_more_than_one_person_in_same_year_and_group(self):
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

        user2 = User.objects.get(username='janedoe')
        group_member2 = GroupMember(
            user = user2,
            group = group,
            is_admin = False
        )
        group_member2.save()

        user3 = User.objects.get(username='alicesmith')
        group_member3 = GroupMember(
            user = user3,
            group = group,
            is_admin = False
        )
        group_member3.save()

        assignment1 = Assignment(
            group = group,
            giver = group_member1.user,
            receiver = group_member2.user,
            year = 2025

        )   
        assignment1.save()

        assignment2 = Assignment(
            group = group,
            giver = group_member1.user,
            receiver = group_member3.user,
            year = 2025

        )   
        self._assert_assignment_is_invalid(assignment2)

    #  test user is not assigned the same person in the next year

    # test user does not receive from from the user they are giving to - ensures no cycles
    # def test_user_does_not_receive_from_user_they_are_giving_to(self):
    #     group = Group(
    #         name = 'Test Group',
    #         code = 'ABCDEFGH',
    #         group_type = 'family',
    #         admin = self.user
    #     )
    #     group.save()

    #     group_member1 = GroupMember(
    #         user = self.user,
    #         group = group,
    #         is_admin = False
    #     )
    #     group_member1.save()

    #     user2 = User.objects.get(username='janedoe')
    #     group_member2 = GroupMember(
    #         user = user2,
    #         group = group,
    #         is_admin = False
    #     )
    #     group_member2.save()

    #     assignment1 = Assignment(
    #         group = group,
    #         giver = group_member1.user,
    #         receiver = group_member2.user,
    #         year = 2025

    #     )   
    #     assignment1.save()

    #     assignment2 = Assignment(
    #         group = group,
    #         giver = group_member2.user,
    #         receiver = group_member1.user,
    #         year = 2025

    #     )   
    #     self._assert_assignment_is_invalid(assignment2)

    # test year cannot be blank
    def test_year_cannot_be_blank(self):
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

        user2 = User.objects.get(username='janedoe')
        group_member2 = GroupMember(
            user = user2,
            group = group,
            is_admin = False
        )
        group_member2.save()

        assignment = Assignment(
            group = group,
            giver = group_member1.user,
            receiver = group_member2.user,
            year = None

        )   
        self._assert_assignment_is_invalid(assignment)

    # test group cannot be blank
    def test_group_cannot_be_blank(self):
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

        user2 = User.objects.get(username='janedoe')
        group_member2 = GroupMember(
            user = user2,
            group = group,
            is_admin = False
        )
        group_member2.save()

        assignment = Assignment(
            group = None,
            giver = group_member1.user,
            receiver = group_member2.user,
            year = 2025

        )   
        self._assert_assignment_is_invalid(assignment)

    def _assert_assignment_is_valid(self, assignment):
        try:
            assignment.full_clean()
        except (ValidationError):
            self.fail('Test assignment should be valid')

    def _assert_assignment_is_invalid(self, assignment):
        with self.assertRaises(ValidationError):
            assignment.full_clean()

    # giver = models.ForeignKey(User, related_name='given_assignments', on_delete=models.CASCADE)  # User who gives the gift
    # receiver = models.ForeignKey(User, related_name='received_assignments', on_delete=models.CASCADE)  # User who receives the gift
    # group = models.ForeignKey(Group, related_name='assignments', on_delete=models.CASCADE)  # Group in which the assignment is made
    # year = models.IntegerField()  # Year of the assignment

    # class Meta:
    #     unique_together = ('giver', 'year', 'group')  # Ensures a user can only give one gift per year per group

    # def __str__(self):
    #     return f"{self.giver.username} -> {self.receiver.username} ({self.year}) in {self.group.name}"
    