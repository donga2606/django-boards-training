from django.core import mail
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

class PasswordResetEmailTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='donga', email='donga.ftu2@gmail.com', password='chuechcon109')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'donga.ftu2@gmail.com'})
    def test_email(self):
        email = mail.outbox[0]
        body = email.body
        subject = email.subject
        uid = self.response.context.get('uid')
        token = self.response.context.get('token')
        password_reset_confirm_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid, 'token': token
        })
        self.assertIn(password_reset_confirm_url, body)
        self.assertEqual('[Django Boards] Please reset your password!', subject)
        self.assertIn('donga.ftu2@gmail.com', body)
        self.assertIn('donga', body)
        self.assertEqual(['donga.ftu2@gmail.com', ], email.to)
