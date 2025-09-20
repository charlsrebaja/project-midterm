from django.urls import path
from . import views

urlpatterns = [
    path('', views.cipher_tools_view, name='cipher_tools'),
    path('process/', views.process_cipher, name='process_cipher'),
]
