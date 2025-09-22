"""
URL configuration for security_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from auth_app.views import dashboard_view, homepage_view

# Import Swagger URL patterns
from .swagger import urlpatterns as swagger_urls

# Custom logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return HttpResponseRedirect(reverse('home'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('auth/', include('auth_app.urls')),
    path('ciphers/', include('ciphers.urls')),
    path('jokes/', include('jokes.urls')),
    path('automation/', include('automation.urls')),
    path('auth/logout/', logout_view, name='logout'),  # Custom logout URL
]

# Add Swagger URL patterns
urlpatterns += swagger_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
