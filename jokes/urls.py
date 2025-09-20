from django.urls import path
from . import views

urlpatterns = [
    path('', views.jokes_dashboard_view, name='jokes_dashboard'),
    path('fetch/', views.fetch_joke, name='fetch_joke'),
]
