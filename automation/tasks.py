from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import requests
from auth_app.models import EmailRecipient, SMSRecipient
from ciphers.utils import CipherUtils
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_joke_emails():
    """
    Celery task to fetch jokes and send them to email recipients
    """
    try:
        # Fetch a joke from JokeAPI
        response = requests.get('https://v2.jokeapi.dev/joke/Any?safe-mode')
        joke_data = response.json()
        
        # Format joke text
        if joke_data.get('type') == 'single':
            joke_text = joke_data.get('joke', '')
        else:
            setup = joke_data.get('setup', '')
            delivery = joke_data.get('delivery', '')
            joke_text = f"{setup}\n\n{delivery}"
        
        # Get active email recipients
        recipients = EmailRecipient.objects.filter(is_active=True)
        
        if recipients.exists():
            # Prepare email content with original and encrypted versions
            atbash_text = CipherUtils.atbash_cipher(joke_text)
            caesar_text = CipherUtils.caesar_cipher(joke_text, shift=3)
            vigenere_text = CipherUtils.vigenere_cipher(joke_text, key="JOKE")
            
            email_content = f"""
            Daily Joke from Security System!
            
            Original Joke:
            {joke_text}
            
            ===== Encrypted Versions =====
            
            Atbash Cipher:
            {atbash_text}
            
            Caesar Cipher (shift=3):
            {caesar_text}
            
            Vigenere Cipher (key=JOKE):
            {vigenere_text}
            
            Category: {joke_data.get('category', 'Unknown')}
            
            Have a great day!
            """
            
            # Send email to each recipient
            for recipient in recipients:
                try:
                    send_mail(
                        subject='Your Daily Joke - Security System',
                        message=email_content,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )
                    logger.info(f"Joke email sent to {recipient.email}")
                except Exception as e:
                    logger.error(f"Failed to send email to {recipient.email}: {str(e)}")
            
            return f"Jokes sent to {recipients.count()} recipients"
        else:
            return "No active email recipients found"
            
    except Exception as e:
        logger.error(f"Error in send_joke_emails task: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def send_joke_sms():
    """
    Celery task to send jokes via SMS (simulated or using Twilio)
    """
    try:
        # Fetch a joke from JokeAPI
        response = requests.get('https://v2.jokeapi.dev/joke/Any?safe-mode')
        joke_data = response.json()
        
        # Format joke text (shorter for SMS)
        if joke_data.get('type') == 'single':
            joke_text = joke_data.get('joke', '')[:160]  # SMS limit
        else:
            setup = joke_data.get('setup', '')
            delivery = joke_data.get('delivery', '')
            joke_text = f"{setup} {delivery}"[:160]
        
        # Get active SMS recipients
        recipients = SMSRecipient.objects.filter(is_active=True)
        
        if recipients.exists():
            for recipient in recipients:
                try:
                    # Simulate SMS sending (replace with actual Twilio integration)
                    logger.info(f"SMS sent to {recipient.phone_number}: {joke_text}")
                    
                    # For actual Twilio integration, uncomment and configure:
                    # from twilio.rest import Client
                    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                    # message = client.messages.create(
                    #     body=joke_text,
                    #     from_=settings.TWILIO_PHONE_NUMBER,
                    #     to=recipient.phone_number
                    # )
                    
                except Exception as e:
                    logger.error(f"Failed to send SMS to {recipient.phone_number}: {str(e)}")
            
            return f"SMS sent to {recipients.count()} recipients"
        else:
            return "No active SMS recipients found"
            
    except Exception as e:
        logger.error(f"Error in send_joke_sms task: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def cleanup_old_sessions():
    """
    Celery task to clean up old sessions
    """
    from django.contrib.sessions.models import Session
    from django.utils import timezone
    
    try:
        expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
        count = expired_sessions.count()
        expired_sessions.delete()
        logger.info(f"Cleaned up {count} expired sessions")
        return f"Cleaned up {count} expired sessions"
    except Exception as e:
        logger.error(f"Error cleaning up sessions: {str(e)}")
        return f"Error: {str(e)}"
