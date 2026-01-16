from secretsanta.forms.create_group_form import CreateGroupForm 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

@login_required
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        print(form.is_bound)
        
        if form.is_valid():
            print("Form is valid")
            form.save(admin=request.user)
            messages.success(request, 'Group created successfully!')
            return redirect('my_groups')  # Redirect to the dashboard or any other page
        else:
            messages.error(request, 'There was an error creating the group.')
    else:
        form = CreateGroupForm()

    return render(request, 'create_group.html', {'form': form})
