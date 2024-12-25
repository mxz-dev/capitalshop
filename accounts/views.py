from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
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

from accounts.forms import CustomAuthenticationForm, DeliveryInfoForm, CustomUserCreationForm, UpdateProfileForm, PaymentInfoForm
from accounts.tokens import account_activation_token
from accounts.models import PaymentInfo, DeliveryInfo
from shop.models import Cart

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
        c = Cart(created_by=user,status="abandoned")
        c.save()
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'email activation is successful')
        return redirect(reverse("shop:home"))
    else:
        return HttpResponse("Activation link is invalid.")

@login_required()
def signout(request):
    logout(request)
    return redirect(reverse("accounts:login"))

@login_required
def update_profile_view(request):
    user = request.user
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile is updated.')
            return redirect('accounts:profile')
    else:
        form = UpdateProfileForm(instance=user)
    return render(request, 'accounts/profile/account_details.html', {"form": form, "user": user})

@login_required()
def billing_view(request):
    cards = PaymentInfo.objects.filter(user=request.user)
    locations = DeliveryInfo.objects.filter(user=request.user)
    payment_form = PaymentInfoForm()
    delivery_form = DeliveryInfoForm()
    return render(request, 'accounts/profile/billing_details.html', {
        'payment_form':payment_form,
        'delivery_form':delivery_form,
        'cards':cards,
        'locations':locations
        })

@login_required
def add_credit_card(request):
    form = PaymentInfoForm()
    if request.method == "POST":
        form = PaymentInfoForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data["card_number"]
            if not PaymentInfo.objects.filter(card_number=card_number, user=request.user).exists():
                card = form.save(commit=False)
                card.user = request.user
                card.save()
                messages.add_message(request, messages.SUCCESS, 'credit card add successfuly.')
            else:
                messages.add_message(request, messages.INFO, 'Dupicate Card! please try another one.')
    return redirect(reverse("accounts:billing"))

@login_required
def add_delivery_info(request):
    form = DeliveryInfoForm()
    if request.method == "POST":
        form = DeliveryInfoForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.save()
            messages.add_message(request, messages.SUCCESS, 'delivery info add successfuly.')
    return redirect(reverse("accounts:billing"))

@login_required()
def delete_card(request, pk):
    card = get_object_or_404(PaymentInfo, user=request.user, pk=pk)
    card.delete()
    return JsonResponse({
        "message": "card removed.",
     })

@login_required()
def delete_address(request, pk):
    addr = get_object_or_404(DeliveryInfo, user=request.user, pk=pk)
    addr.delete()
    return JsonResponse({
        "message": "Delivery info removed.",
     })

@login_required()
def security_view(request):
    return render(request, 'accounts/profile/account_security.html')

