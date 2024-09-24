from django.http import HttpResponse
from secretsanta.forms.sign_up_form import SignUpForm
from secretsanta.forms.log_in_form import LogInForm 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

# Create your views here.
def home(request):
    return render(request, 'home.html') 

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def log_in(request):

    if request.method == "POST": # checks method request
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
    form = LogInForm()
    return render(request, 'log_in.html', {'form' : form})

def dashboard(request):
    return render(request, 'dashboard.html') 