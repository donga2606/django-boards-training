from ..templatetags.form_tags import field_type, input_class
from django.test import TestCase
from django import forms

class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ['name', 'password']

class FieldTypeTest(TestCase):
    def test_field_type_widget(self):
        form = ExampleForm()
        self.assertEquals('TextInput', field_type(form['name']))
        self.assertEquals('PasswordInput', field_type(form['password']))

class InputClassTest(TestCase):
    def test_unbound_data(self):
        form = ExampleForm()
        self.assertEquals('form-control ', input_class(form['name']))
        self.assertEquals('form-control ', input_class(form['password']))
    def test_bound_data_valid(self):
        form = ExampleForm({'name': 'donga', 'password': '123'})
        self.assertEquals('form-control is-valid', input_class(form['name']))
        self.assertEquals('form-control ', input_class(form['password']))
    def test_bound_data_invalid(self):
        form = ExampleForm({'name': '','password': '1234'})
        self.assertEquals('form-control is-invalid', input_class(form['name']))


