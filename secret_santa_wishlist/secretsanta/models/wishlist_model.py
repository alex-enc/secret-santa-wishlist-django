from django.db import models
from django.contrib.auth.models import AbstractUser  
from .user_model import User
from .group_model import Group

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="wishlists")
    published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "group")  # Ensures each user has only one wishlist per group
