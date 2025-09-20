from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TwoFactorForm
from .models import User
import pyotp
import qrcode
from io import BytesIO
import base64
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from datetime import timedelta

# Homepage view
def homepage_view(request):
    """Display the homepage for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'homepage.html')

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                # Generate OTP secret for 2FA
                user.otp_secret = pyotp.random_base32()
                user.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}! Please login.')
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'An error occurred during registration. Please try again.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth_app/register.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        
        # Check if user exists and is locked
        try:
            user = User.objects.get(username=username)
            
            # Check if account is locked
            if user.is_locked:
                # Check if lockout period has passed (30 minutes)
                if user.lockout_until and timezone.now() > user.lockout_until:
                    # Unlock the account
                    user.reset_failed_attempts()
                else:
                    remaining_time = (user.lockout_until - timezone.now()).seconds // 60
                    messages.error(request, f'Account is locked. Try again in {remaining_time} minutes.')
                    return render(request, 'auth_app/login.html', {'form': form})
            
            if form.is_valid():
                # Reset failed attempts on successful login
                user.reset_failed_attempts()
                
                user = form.get_user()
                
                # Check if 2FA is enabled
                if user.is_two_factor_enabled:
                    request.session['pre_2fa_user_pk'] = user.pk
                    return redirect('verify_2fa')
                else:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('dashboard')
            else:
                # Increment failed attempts
                user.increment_failed_login()
                
                if user.is_locked:
                    messages.error(request, 'Account locked due to multiple failed login attempts. Try again in 30 minutes.')
                else:
                    remaining_attempts = 3 - user.failed_login_attempts
                    messages.error(request, f'Invalid credentials. {remaining_attempts} attempts remaining.')
                    
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth_app/login.html', {'form': form})

@csrf_protect
def verify_2fa_view(request):
    user_pk = request.session.get('pre_2fa_user_pk')
    if not user_pk:
        return redirect('login')
    
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return redirect('login')
    
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            totp = pyotp.TOTP(user.otp_secret)
            
            if totp.verify(token, valid_window=1):
                login(request, user)
                del request.session['pre_2fa_user_pk']
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid 2FA token. Please try again.')
    else:
        form = TwoFactorForm()
    
    return render(request, 'auth_app/verify_2fa.html', {'form': form})

@login_required
def setup_2fa_view(request):
    user = request.user
    
    if user.is_two_factor_enabled:
        messages.info(request, '2FA is already enabled for your account.')
        return redirect('dashboard')
    
    # Ensure user has an OTP secret
    if not user.otp_secret:
        user.otp_secret = pyotp.random_base32()
        user.save()
    
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            totp = pyotp.TOTP(user.otp_secret)
            
            if totp.verify(token, valid_window=1):
                user.is_two_factor_enabled = True
                user.save()
                messages.success(request, '2FA has been successfully enabled!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid token. Please try again.')
    else:
        form = TwoFactorForm()
    
    # Generate QR code
    totp_uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(
        name=user.username,
        issuer_name='Security System'
    )
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    context = {
        'form': form,
        'qr_code': qr_code,
        'secret': user.otp_secret
    }
    
    return render(request, 'auth_app/setup_2fa.html', context)

@login_required
def disable_2fa_view(request):
    user = request.user
    
    if not user.is_two_factor_enabled:
        messages.info(request, '2FA is not enabled for your account.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            totp = pyotp.TOTP(user.otp_secret)
            
            if totp.verify(token, valid_window=1):
                user.is_two_factor_enabled = False
                # Generate new secret for next time
                user.otp_secret = pyotp.random_base32()
                user.save()
                messages.success(request, '2FA has been disabled.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid token. Please try again.')
    else:
        form = TwoFactorForm()
    
    return render(request, 'auth_app/disable_2fa.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    # Explicitly redirect to the homepage, not login page
    # Use HttpResponseRedirect instead of redirect to ensure an HttpResponse is returned
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    return HttpResponseRedirect(reverse('home'))
