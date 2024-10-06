from django import forms
from secretsanta.models import Group
import string
import random

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']  # Only the group name is required from the user

    def save(self, commit=True, admin=None):
        """Create a new group with a random unique code and set the admin."""
        
        group = super().save(commit=False)
        group.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # Generate random code
        
        # Assign the admin if provided
        if admin:
            group.admin = admin

        if commit:
            group.save()
            group.members.add(admin)  # Add the admin as the first group member
        return group
