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
        ('family', 'Family'),
        ('friends', 'Friends'),
        ('work', 'Work'),
    ]

    name = models.CharField(max_length=100, unique=False)  # Group name
    code = models.CharField(max_length=8, unique=True, blank=False)  # Random unique code
    group_type = models.CharField(max_length=20, choices=GROUP_TYPE_CHOICES, default='family_friends')
    admin = models.ForeignKey(User, related_name='admin_groups', on_delete=models.CASCADE)  # Admin who created the group

class GroupMember(models.Model):
    user = models.ForeignKey(User, related_name="memberships", on_delete=models.CASCADE)  # Links to User model
    group = models.ForeignKey(Group, related_name="memberships", on_delete=models.CASCADE)  # Links to Group model
    date_joined = models.DateTimeField(auto_now_add=True)  # When the user joined the group
    is_admin = models.BooleanField(default=False)  # Whether the user is an admin of the group

    class Meta:
        unique_together = ('user', 'group')  # Ensures a user cannot join the same group twice

    def __str__(self):
        return f"{self.group.name} -- Code: {self.group.code}"


class Assignment(models.Model):
    giver = models.ForeignKey(User, related_name='given_assignments', on_delete=models.CASCADE)  # User who gives the gift
    receiver = models.ForeignKey(User, related_name='received_assignments', on_delete=models.CASCADE)  # User who receives the gift
    group = models.ForeignKey(Group, related_name='assignments', on_delete=models.CASCADE)  # Group in which the assignment is made
    year = models.IntegerField()  # Year of the assignment

    class Meta:
        unique_together = ('giver', 'year', 'group')  # Ensures a user can only give one gift per year per group

    def __str__(self):
        return f"{self.giver.username} -> {self.receiver.username} ({self.year}) in {self.group.name}"
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="wishlists")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "group")  # Ensures each user has only one wishlist per group

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=255)
    item_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    taken = models.BooleanField(default=False)  # Whether the item has been taken by a giver
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.item_name   
    