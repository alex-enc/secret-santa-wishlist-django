from django import forms

class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    new_password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())