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
    name = models.CharField(max_length=100, unique=False)  # Group name
    code = models.CharField(max_length=8, unique=True, blank=False)  # Random unique code
    # users = models.ManyToManyField('User', related_name='user_groups')  # Group members
    admin = models.ForeignKey(User, related_name='admin_groups', on_delete=models.CASCADE)  # Admin who created the group
