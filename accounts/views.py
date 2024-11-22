from django.shortcuts import render, redirect
from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.urls import reverse
# Create your views here.
def login_view(request):
    form = CustomAuthenticationForm()
    if request.method == "POST":
        form = CustomAuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            messages.add_message(request, messages.SUCCESS, 'Registration Complete. Check Your Inbox.')
        else:
            print(form.error_messages)
    return render(request, 'accounts/login.html', {'form':form})
def registration_view(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Registration Complete. Check Your Inbox.')
            return redirect(reverse("accounts:login"))
    return render(request, 'accounts/registration.html', {"form":form})