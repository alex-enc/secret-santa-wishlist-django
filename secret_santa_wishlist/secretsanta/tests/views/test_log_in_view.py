""" Test of the log in view """
from django.test import TestCase
from django.urls import reverse
from secretsanta.forms.log_in_form import LogInForm
from django.test import TestCase
from secretsanta.models import User
from django.contrib.auth.hashers import check_password

def test_is_logged_in(self):
    return '_auth_user_id' in self.client.session.keys()

def test_successful_log_in(self):
    form_input = {'username' : 'johndoe',
                  'password' : 'Password123'
                  }
    response = self.client.post(self.url, form_input, follow=True)
    self.assertTrue(self._is_logged_in())
    response_url = reverse('dashboard')
    self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    self.assertTemplateUsed(response, 'dashboard.html')