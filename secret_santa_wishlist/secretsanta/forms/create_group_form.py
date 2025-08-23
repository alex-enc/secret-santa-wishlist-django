from django import forms
from secretsanta.models import Group, GroupMember
import string
import random
from django.contrib.auth import get_user_model

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'group_type']  # includes group_type and name of the group
        # fields = ['group_type, name']  # includes group_type and name of the group
        widgets = {
            'group_type': forms.Select(attrs={'class': 'form-select'}),
        }
    # def __init__(self, *args, **kwargs):
    #     self.admin_user = kwargs.pop('admin', None)
    #     super().__init__(*args, **kwargs)

    def save(self, commit=True, admin=None):
        """Create a new group with a random unique code and set the admin."""
 
        super().save(commit=False)
        group = Group(
            name=self.cleaned_data.get('name'),
            group_type=self.cleaned_data.get('group_type'),
            code=''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
        )
        if admin:
            group.admin = admin

        if commit:
            group.save()
            # ✅ Add admin as first member
            GroupMember.objects.create(group=group, user=admin, is_admin=True)
        # group.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # Generate random code
        
        # Assign the admin since they are creating the group
        # group.admin = self.admin_user

        # if commit:
        #     group.save()
        #     group.members.add(admin)  # Add the admin as the first group member
        return group


        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
        )
        return user
