from django import forms
from .models import Topic, Post



class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Whats in your mind', 'rows': 10}), max_length=4000, help_text='the max length is 4000')
    class Meta:
        model = Topic
        fields = ['subject', 'message']

class PostForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Whats in your mind', 'rows': 10}),
                              max_length=4000, help_text='the max length is 4000')
    class Meta:
        fields = ['message']

