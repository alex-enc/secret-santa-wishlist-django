""" Test of the sign up view """
from django.test import TestCase
from django.urls import reverse
from secretsanta.forms import SignUpForm
from django.test import TestCase
from secretsanta.models import User
from django.contrib.auth.hashers import check_password


class SignUpViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input ={
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
        }

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def test_sign_up_url(self):
        self.assertEqual(self.url,'/sign_up/')

    def test_get_sign_up(self):
        url = reverse('sign_up')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesful_sign_up(self):
        self.form_input['email'] = 'INCORRECT_EMAIL'
        count_before = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        count_after = User.objects.count()
        self.assertEqual(count_after, count_before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_succesful_sign_up(self):
        count_before = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
            # Print form errors if the user count doesn't increase
        if User.objects.count() == count_before:
            print(response.context['form'].errors)
        count_after = User.objects.count()
        self.assertEqual(count_after, count_before+1)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        user = User.objects.get(email='johndoe@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'johndoe@example.com')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())

