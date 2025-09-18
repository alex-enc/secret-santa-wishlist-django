from django import forms
from django.core.validators import RegexValidator
from secretsanta.models import  GroupMember

class JoinGroupForm(forms.Form):
    """Form enabling users to join a existing group"""
    group_code = forms.CharField(label="Group code")



    # search GroupMember and add that user to that list.


    # def save(self, commit=True, admin=None):
    #     """Create a new group with a random unique code and set the admin."""
 
    #     super().save(commit=False)
    #     group = Group(
    #         name=self.cleaned_data.get('name'),
    #         group_type=self.cleaned_data.get('group_type'),
    #         code=''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
    #     )


    #     if commit:
    #         group.save()
    #         # Add admin as first member
            
    #         GroupMember.objects.create(group=group, user=admin, is_admin=True)
    #         if admin:   
    #             group.members.add(admin)  # ensure admin is a member too
    #     return group
