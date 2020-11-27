from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class PasswordResetView(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)
        self.form = self.response.context.get('form')
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_resolve(self):
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)
    def test_contain_form(self):
        self.assertIsInstance(self.form, auth_views.PasswordResetForm)
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    def test_form_input(self):
        self.assertContains(self.response, '<input ', 2)
        self.assertContains(self.response, 'type="email"', 1)



class SuccessfulPasswordReset(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        User.objects.create_user(username='donga123', email='donga.ftu2@gmail.com', password='naruto321')
        self.response = self.client.post(url, {'email': 'donga.ftu2@gmail.com'})

    def test_redirection(self):
        url_done_view = reverse('password_reset_done')
        self.assertRedirects(self.response, url_done_view)
    def test_sent_email(self):
        self.assertEqual(1, len(mail.outbox))

class InvalidEmailPasswordReset(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        User.objects.create_user(username='donga123', email='donga.ftu2@gmail.com', password='naruto321')
        self.response = self.client.post(url, {'email': 'donotexit@gmail.com'})
    def test_redirection(self):
        url_done = reverse('password_reset_done')
        self.assertRedirects(self.response, url_done)
    def test_email_no_send(self):
        self.assertEqual(0, len(mail.outbox))

class PasswordResetDoneTest(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_resolve(self):
        view = resolve('/reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)

class PasswordResetConfirmTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='donga', email='donga.ftu2@gmail.com',password='2434353qwjhdfd')
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)
        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_function(self):
        view = resolve('/reset/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    def test_input(self):
        self.assertContains(self.response, '<input ', 3)
        self.assertContains(self.response, 'type="password"', 2)
    def test_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, auth_views.SetPasswordForm)

class InvalidPasswordResetConfirmTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='donga', email='donga.ftu2@gmail.com', password='2434353qwjhdfd')
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)
        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        user.set_password('sghcbs12331')
        user.save()
        self.response = self.client.get(url, follow=True)
    def test_status(self):
        self.assertEquals(self.response.status_code, 200)
    def test_invalid_template(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))



