from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from secretsanta.forms.sign_up_form import SignUpForm
from secretsanta.forms.log_in_form import LogInForm 
from secretsanta.forms.create_group_form import CreateGroupForm 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html') 

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.is_bound)
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})



def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Change 'dashboard' to your redirect URL
            else:
                messages.error(request, 'Invalid username or password.')  # Add error message
        else:
            messages.error(request, 'Please correct the error below.')  # For form errors

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def dashboard(request):
    return render(request, 'dashboard.html') 

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

@login_required
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        print(form.is_bound)
        if form.is_valid():
            print("Form is valid")
            # group = form.cleaned_data['group']
            # group = form.save()
            group = form.save(admin=request.user)
            # form.save()  # Set the logged-in user as the admin
            messages.success(request, 'Group created successfully!')
            return redirect('create_group')  # Redirect to the dashboard or any other page
        else:
            messages.error(request, 'There was an error creating the group.')
    else:
        form = CreateGroupForm()

    return render(request, 'create_group.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')