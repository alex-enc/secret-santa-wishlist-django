from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_model import User
from .group_model import Group

class GroupMember(models.Model):
    user = models.ForeignKey(User, related_name="memberships", on_delete=models.CASCADE)  # Links to User model
    group = models.ForeignKey(Group, related_name="memberships", on_delete=models.CASCADE)  # Links to Group model
    date_joined = models.DateTimeField(auto_now_add=True)  # When the user joined the group
    is_admin = models.BooleanField(default=False)  # Whether the user is an admin of the group

    class Meta:
        unique_together = ('user', 'group')  # Ensures a user cannot join the same group twice

    def __str__(self):
        return f"{self.group.name} -- Code: {self.group.code}"
