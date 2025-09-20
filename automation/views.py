from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from auth_app.models import EmailRecipient, SMSRecipient
from .tasks import send_joke_emails, send_joke_sms
import json
import requests


# Temporarily removed login_required for testing
def automation_dashboard(request):
    """Automation dashboard view"""
    email_recipients = EmailRecipient.objects.all()
    
    context = {
        'email_recipients': email_recipients,
    }
    return render(request, 'automation/dashboard.html', context)


@login_required
def add_email_recipient(request):
    """Add email recipient"""
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        
        if email and name:
            try:
                EmailRecipient.objects.create(email=email, name=name)
                messages.success(request, f'Email recipient {name} added successfully!')
            except Exception as e:
                messages.error(request, f'Error adding recipient: {str(e)}')
        else:
            messages.error(request, 'Please provide both name and email.')
        
        return redirect('automation_dashboard')
    
    return render(request, 'automation/add_email.html')




@login_required
def toggle_recipient_status(request, recipient_type, recipient_id):
    """Toggle recipient active status"""
    try:
        if recipient_type == 'email':
            recipient = EmailRecipient.objects.get(id=recipient_id)
        else:
            recipient = SMSRecipient.objects.get(id=recipient_id)
        
        recipient.is_active = not recipient.is_active
        recipient.save()
        
        status = 'activated' if recipient.is_active else 'deactivated'
        messages.success(request, f'Recipient {recipient.name} {status}.')
    except Exception as e:
        messages.error(request, f'Error toggling status: {str(e)}')
    
    return redirect('automation_dashboard')


@login_required
def delete_recipient(request, recipient_type, recipient_id):
    """Delete recipient"""
    try:
        if recipient_type == 'email':
            recipient = EmailRecipient.objects.get(id=recipient_id)
        else:
            recipient = SMSRecipient.objects.get(id=recipient_id)
        
        name = recipient.name
        recipient.delete()
        messages.success(request, f'Recipient {name} deleted.')
    except Exception as e:
        messages.error(request, f'Error deleting recipient: {str(e)}')
    
    return redirect('automation_dashboard')


# Temporarily removed login_required for testing
def trigger_email_task(request):
    """Manually trigger email sending task"""
    try:
        # Run the task synchronously instead of asynchronously
        result = send_joke_emails()
        return JsonResponse({
            'success': True,
            'message': 'Email task triggered successfully!',
            'result': result
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })




# Temporarily removed login_required for testing
def trigger_joke_api(request):
    """Manually fetch a joke from the API and return it"""
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
        
        return JsonResponse({
            'success': True,
            'joke': joke_text,
            'category': joke_data.get('category', 'Unknown')
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
