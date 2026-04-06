from .forms.join_group_form import JoinGroupForm
from .forms.create_group_form import CreateGroupForm

def join_group_form(request):
    return {
        'join_group_form': JoinGroupForm()
    }

def create_group_form(request):
    return {
        'create_group_form': CreateGroupForm()
    }