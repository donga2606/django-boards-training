from django.test import TestCase
from ..form import SignUpForm
from django.urls import resolve, reverse
from ..views import sign_up
from django.contrib.auth.models import User
# Create your tests here.


class SignUpTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_resolve(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, sign_up)
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    def test_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SignUpForm)
    def test_form_input(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)
        self.assertContains(self.response, 'type="text"', 1)

class SuccessSignUpTest(TestCase):
    def setUp(self):
        data ={
            'username': 'donga',
            'email': 'dongaftu2@gmail.com',
            'password1': 'abcdf123456',
            'password2': 'abcdf123456',
        }
        signup_url = reverse('signup')
        self.home_url = reverse('home')
        self.response = self.client.post(signup_url, data)

    def test_user_create(self):
        self.assertTrue(User.objects.exists())

    def test_redirect(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignUpTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_errors_note(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    def test_fail_creating_user(self):
        self.assertFalse(User.objects.exists())


















