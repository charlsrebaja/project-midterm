from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    """Custom User model with additional security features"""
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    lockout_until = models.DateTimeField(null=True, blank=True)
    
    # 2FA fields
    is_two_factor_enabled = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=32, blank=True)
    
    # Profile fields
    phone_number = models.CharField(max_length=15, blank=True)
    
    def increment_failed_login(self):
        """Increment failed login attempts and lock if necessary"""
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        
        if self.failed_login_attempts >= 3:
            self.is_locked = True
            self.lockout_until = timezone.now() + timedelta(minutes=30)
        
        self.save()
    
    def reset_failed_attempts(self):
        """Reset failed login attempts on successful login"""
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.is_locked = False
        self.lockout_until = None
        self.save()
    
    def is_lockout_expired(self):
        """Check if lockout period has expired"""
        if self.lockout_until and timezone.now() > self.lockout_until:
            self.reset_failed_attempts()
            return True
        return False
    
    class Meta:
        db_table = 'auth_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class EmailRecipient(models.Model):
    """Model to store email recipients for automation"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    class Meta:
        db_table = 'email_recipients'
        verbose_name = 'Email Recipient'
        verbose_name_plural = 'Email Recipients'


class SMSRecipient(models.Model):
    """Model to store SMS recipients for automation"""
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.phone_number})"
    
    class Meta:
        db_table = 'sms_recipients'
        verbose_name = 'SMS Recipient'
        verbose_name_plural = 'SMS Recipients'
