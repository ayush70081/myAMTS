from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

class AdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if this is an admin URL
        is_admin = request.path.startswith('/admin/')
        
        # Set different session cookie names for admin and main site
        if is_admin:
            settings.SESSION_COOKIE_NAME = 'admin_sessionid'
        else:
            settings.SESSION_COOKIE_NAME = 'main_sessionid'
            
        response = self.get_response(request)
        
        # Set the correct path for the session cookie
        if is_admin:
            if 'admin_sessionid' in response.cookies:
                response.cookies['admin_sessionid']['path'] = '/admin/'
        else:
            if 'main_sessionid' in response.cookies:
                response.cookies['main_sessionid']['path'] = '/'
                
        return response
