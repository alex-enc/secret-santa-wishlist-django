from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username =  models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, blank=False)

# Group Model
class Group(models.Model):
    GROUP_TYPE_CHOICES = [
        ('family_friends', 'Family & Friends'),
        ('work', 'Work'),
    ]

    name = models.CharField(max_length=100, unique=False)  # Group name
    code = models.CharField(max_length=8, unique=True, blank=False)  # Random unique code
    # users = models.ManyToManyField('User', related_name='user_groups')  # Group members
    group_type = models.CharField(max_length=20, choices=GROUP_TYPE_CHOICES, default='family_friends')
    admin = models.ForeignKey(User, related_name='admin_groups', on_delete=models.CASCADE)  # Admin who created the group

    def __str__(self):
        return f"{self.name} ({self.get_group_type_display()})"
    
class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to User model
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # Links to Group model
    date_joined = models.DateTimeField(auto_now_add=True)  # When the user joined the group
    is_admin = models.BooleanField(default=False)  # Whether the user is an admin of the group

    class Meta:
        unique_together = ('user', 'group')  # Ensures a user cannot join the same group twice

    def __str__(self):
        return f"{self.user.username} in {self.group.name} (Code: {self.group.code})"