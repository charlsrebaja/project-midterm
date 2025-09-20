from django.urls import path
from . import views

urlpatterns = [
    path('', views.automation_dashboard, name='automation_dashboard'),
    path('add-email/', views.add_email_recipient, name='add_email_recipient'),
    path('toggle/<str:recipient_type>/<int:recipient_id>/', views.toggle_recipient_status, name='toggle_recipient'),
    path('delete/<str:recipient_type>/<int:recipient_id>/', views.delete_recipient, name='delete_recipient'),
    path('trigger-email/', views.trigger_email_task, name='trigger_email_task'),
    path('trigger-joke/', views.trigger_joke_api, name='trigger_joke_api'),
]
