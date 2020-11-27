from django.shortcuts import render, redirect
from .form import SignUpForm
from django.contrib.auth import login as auth_login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.models import User

# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    template_name = 'my_account.html'
    fields = ('first_name', 'last_name', 'email', )
    success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user
