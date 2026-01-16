from secretsanta.forms.create_group_form import CreateGroupForm 
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def new_group_info(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.save(admin=request.user)  # Set the logged-in user as the admin
            messages.success(request, 'Group created successfully!')
            return redirect('dashboard')  # Redirect to the dashboard or any other page
        else:
            messages.error(request, 'There was an error creating the group.')
    else:
        form = CreateGroupForm()

    return render(request, 'new_group_info.html', {'form': form})
