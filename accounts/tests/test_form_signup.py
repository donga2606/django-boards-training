from django.test import TestCase
from ..form import SignUpForm
class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2']
        self.assertSequenceEqual(list(form.fields), expected)
