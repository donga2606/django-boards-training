from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

class LoginRequiredPasswordChangeTest(TestCase):
    def test_login_redirection(self):
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

class PasswordChangeSetUp(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='donga', email='donga.ftu2@gmail.com', password='old_password')
        self.client.login(username='donga', password='old_password')
        url = reverse('password_change')
        self.response = self.client.post(url, data)


class SuccessfulPasswordChange(PasswordChangeSetUp):
    def setUp(self):
        super().setUp(
            {'old_password': 'old_password', 'new_password1': 'new_password', 'new_password2': 'new_password'}
        )
    def test_redirection(self):
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_old_new_password(self):
        self.assertTrue(self.user.check_password('old_password'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authenticated(self):
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidPasswordChange(PasswordChangeSetUp):
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_form(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)





