from django.utils.deprecation import MiddlewareMixin

class AdminSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            # Cambiar la cookie de sesión para el panel de administración
            request.session_cookie_name = 'admin_sessionid'