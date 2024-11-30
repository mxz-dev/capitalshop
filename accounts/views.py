from django.shortcuts import render, redirect
from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

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
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Registration Complete. Check Your Inbox.')
            return redirect(reverse("accounts:login"))
    return render(request, 'accounts/registration.html', {"form":form})

@login_required()
def signout(request):
    logout(request)
    return redirect(reverse("accounts:login"))