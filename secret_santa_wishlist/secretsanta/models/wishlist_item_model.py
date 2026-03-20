from django.db import models
from django.contrib.auth.models import AbstractUser  
from .wishlist_model import Wishlist

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=255)
    item_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    taken = models.BooleanField(default=False)  # Whether the item has been taken by a giver
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.item_name   
    