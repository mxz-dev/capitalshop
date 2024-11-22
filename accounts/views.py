from django.shortcuts import render
from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib import messages
# Create your views here.
def login_view(request):

    return render(request, 'accounts/login.html')
def registration_view(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Registration Complete. Check Your Inbox.')
    return render(request, 'accounts/registration.html', {"form":form})