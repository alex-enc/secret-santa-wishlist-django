from secretsanta.forms.log_in_form import LogInForm 
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard') 
            else:
                messages.error(request, 'Invalid username or password.')  # Add error message
        else:
            messages.error(request, 'Please correct the error below.')  # For form errors

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})