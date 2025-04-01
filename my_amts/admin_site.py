from django.contrib.admin import AdminSite
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import LoginView

class MyAdminSite(AdminSite):
    def login(self, request, extra_context=None):
        """
        Override the login to use a custom session."""
        if request.method == 'POST':
            request.session = {}  # Create new session for admin
        return super().login(request, extra_context)

admin_site = MyAdminSite(name='my_admin')
