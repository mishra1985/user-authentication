from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, ForgotPasswordForm

def triple_forms_view(request):
    login_form = LoginForm()
    reg_form = RegistrationForm()
    forgot_form = ForgotPasswordForm()
    return render(request, 'accounts/tripleforms.html', {
        'login_form': login_form,
        'reg_form': reg_form,
        'forgot_form': forgot_form,
    })

def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            reg_form = RegistrationForm()
            forgot_form = ForgotPasswordForm()
            return render(request, 'accounts/tripleforms.html', {
                'login_form': login_form,
                'reg_form': reg_form,
                'forgot_form': forgot_form,
            })
    return redirect('triple_forms')

def register_view(request):
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            print(f"User {user.username} created successfully.")
            login(request, user)
            if request.user.is_authenticated:
                print(f"User {request.user.username} is now logged in.")
            else:
                print("Login failed after registration.")
            return redirect('dashboard')
        else:
            print("Registration form errors:", reg_form.errors)
            login_form = LoginForm()
            forgot_form = ForgotPasswordForm()
            return render(request, 'accounts/tripleforms.html', {
                'login_form': login_form,
                'reg_form': reg_form,
                'forgot_form': forgot_form,
            })
    return redirect('triple_forms')

def forgot_password_view(request):
    if request.method == 'POST':
        forgot_form = ForgotPasswordForm(request.POST)
        if forgot_form.is_valid():
            username = forgot_form.cleaned_data['username']
            email = forgot_form.cleaned_data['email']
            new_password = forgot_form.cleaned_data['new_password1']
            try:
                user = User.objects.get(username=username, email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password updated successfully. Please log in with your new password.")
                return redirect('login')
            except User.DoesNotExist:
                forgot_form.add_error(None, "No user found with the provided username and email.")
    else:
        forgot_form = ForgotPasswordForm()
    login_form = LoginForm()
    reg_form = RegistrationForm()
    return render(request, 'accounts/tripleforms.html', {
         'login_form': login_form,
         'reg_form': reg_form,
         'forgot_form': forgot_form,
    })

@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('triple_forms')

def home_view(request):
    return render(request, 'accounts/tripleforms.html')
