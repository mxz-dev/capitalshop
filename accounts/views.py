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

from accounts.forms import CustomAuthenticationForm, UpdateUserPasswordForm, DeliveryInfoForm, CustomUserCreationForm, UpdateProfileForm, PaymentInfoForm
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
            return JsonResponse({'success': True, 'message': 'Profile is updated.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
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
                return JsonResponse({'success': True, 'message': 'Credit card added successfully.'})
            else:
                return JsonResponse({'success': False, 'errors':{'errors':['Duplicate card! Please try another one.']}})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
def add_delivery_info(request):
    form = DeliveryInfoForm()
    if request.method == "POST":
        form = DeliveryInfoForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.save()
            return JsonResponse({'success': True, 'message': 'Delivery info added successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})  
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

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
    form = UpdateUserPasswordForm()
    return render(request, 'accounts/profile/account_security.html', {"form": form})

@login_required
def delete_user(request):
    user = User.objects.get(pk=request.user.pk)
    user.delete()
    return JsonResponse({'success': True, 'message': 'User deleted successfully.'})

@login_required
def update_user_password(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = UpdateUserPasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data.get("current_password")
            new_password = form.cleaned_data.get("new_password")
            new_passsword_confirm = form.cleaned_data.get("new_password_confirm")
            if user.check_password(current_password):
                if new_password == new_passsword_confirm:
                    user.set_password(new_password)
                    user.save()
                    return JsonResponse({'success': True, 'message': 'Password updated successfully.'})
                else:
                    return JsonResponse({'success': False, 'message': 'New passwords do not match.'})
            else:
                return JsonResponse({'success': False, 'message': 'Current password is incorrect.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})