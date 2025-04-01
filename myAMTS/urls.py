"""myAMTS URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Restore default admin
    path('', include('my_amts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
