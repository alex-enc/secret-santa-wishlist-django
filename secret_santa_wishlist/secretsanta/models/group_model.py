from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_model import User

# Group Model
class Group(models.Model):
    GROUP_TYPE_CHOICES = [
        ('family', 'Family'),
        ('friends', 'Friends'),
        ('work', 'Work'),
    ]

    name = models.CharField(max_length=100, unique=False)  # Group name
    code = models.CharField(max_length=8, unique=True, blank=False)  # Random unique code
    group_type = models.CharField(max_length=20, choices=GROUP_TYPE_CHOICES, default='family_friends')
    admin = models.ForeignKey(User, related_name='admin_groups', on_delete=models.CASCADE)  # Admin who created the group
