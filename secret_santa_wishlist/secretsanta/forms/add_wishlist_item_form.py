from django import forms
from secretsanta.models import Wishlist, WishlistItem

class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ["item_name", "item_url", "description"]
        widgets = {
            "description": forms.Textarea(),
        }

    def save(self, commit=True, wishlist=None):
        """Create a new wishlist item linked to the given wishlist."""
        super().save(commit=False)
        wishlist_item = WishlistItem(
            wishlist=wishlist,
            item_name=self.cleaned_data.get("item_name"),
            item_url=self.cleaned_data.get("item_url"),
            description=self.cleaned_data.get("description"),)
        if commit:
            wishlist_item.save()
        '''create new wishlist if it is the first time user is adding an item to wishlist'''
        # wishlist, created = Wishlist.objects.get_or_create(
        #     user=user,
        #     group=group,
        # )   
        return wishlist_item
    
