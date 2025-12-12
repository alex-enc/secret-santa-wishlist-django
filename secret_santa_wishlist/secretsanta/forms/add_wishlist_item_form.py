from django import forms
from secretsanta.models import WishlistItem

class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ["item_name", "item_url", "description"]
        widgets = {
            "description": forms.Textarea(),
        }