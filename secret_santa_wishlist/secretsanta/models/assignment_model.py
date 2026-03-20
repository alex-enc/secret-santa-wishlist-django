from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_model import User
from .group_model import Group


class Assignment(models.Model):
    giver = models.ForeignKey(User, related_name='given_assignments', on_delete=models.CASCADE)  # User who gives the gift
    receiver = models.ForeignKey(User, related_name='received_assignments', on_delete=models.CASCADE)  # User who receives the gift
    group = models.ForeignKey(Group, related_name='assignments', on_delete=models.CASCADE)  # Group in which the assignment is made
    year = models.IntegerField()  # Year of the assignment

    class Meta:
        unique_together = ('giver', 'year', 'group')  # Ensures a user can only give one gift per year per group

    def __str__(self):
        return f"{self.giver.username} -> {self.receiver.username} ({self.year}) in {self.group.name}"
    