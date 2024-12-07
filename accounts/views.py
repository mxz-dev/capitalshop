from django.shortcuts import render, redirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm, UpdateProfileForm
from accounts.tokens import account_activation_token

def login_view(request):
    if request.user.is_authenticated != True: 
        form = CustomAuthenticationForm()
        if request.method == "POST":
            form = CustomAuthenticationForm(request=request,data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect(reverse("shop:home"))
        return render(request, 'accounts/login.html', {'form':form})
    else:
        return redirect(reverse("shop:home"))

def registration_view(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            message = render_to_string('accounts/verification/activation.html', {
                'user': user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                'Account Activation Link',
                message,
                to=[to_email],
            )
            email.send()
            messages.add_message(request, messages.SUCCESS, 'registration was successful, please verify your email.')
            return redirect(reverse("accounts:login"))
    return render(request, 'accounts/registration.html', {"form":form})

def activation_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)   
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    active = account_activation_token.check_token(user, token)
    if user and active:
        user.is_active = True
        user.save()
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'email activation is successful')
        return redirect(reverse("shop:home"))
    else:
        return HttpResponse("Activation link is invalid.")

@login_required()
def signout(request):
    logout(request)
    return redirect(reverse("accounts:login"))

@login_required()
def dashboard_view(request):
    form = UpdateProfileForm()
    user = User.objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=user) # update the user instance. 
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile is Updated.')
        
    return render(request, 'accounts/profile/account_details.html', {"form":form, "user":user})

@login_required()
def billing_view(request):
    return render(request, 'accounts/profile/billing_details.html')

@login_required()
def security_view(request):
    return render(request, 'accounts/profile/account_security.html')

