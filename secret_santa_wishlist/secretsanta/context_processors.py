from .forms.join_group_form import JoinGroupForm

def join_group_form(request):
    return {
        'join_group_form': JoinGroupForm()
    }