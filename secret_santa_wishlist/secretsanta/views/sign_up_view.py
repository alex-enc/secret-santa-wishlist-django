from secretsanta.forms.sign_up_form import SignUpForm
from django.shortcuts import redirect, render
from django.contrib.auth import login

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