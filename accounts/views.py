from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            return render(request, 'accounts/signup.html')

def reset_password(request):
    if request.method == 'GET':
        return render(request, 'accounts/password_reset.html')
    elif request.method == 'POST':
        form = PasswordResetForm(request.POST)
        # email = request.POST["email"]
        if form.is_valid():
            form.save(domain_override="127.0.0.1:8000")
            return render(request, 'accounts/check_email.html')
        else:
            return render(request, 'accounts/password_reset.html')

#
# class CustomPasswordResetView(PasswordResetView):
#     email_template_name = 'registration/password_reset_email.html'
#     success_url = reverse_lazy('password_reset_done')
#     template_name = 'registration/password_reset_form.html'