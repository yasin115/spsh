from Product.models import IpAddress
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

class SaveIpAddressMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # استفاده از Lazy Object برای جلوگیری از query زودهنگام
        request.user_ip = SimpleLazyObject(lambda: self.get_user_ip(request))
        response = self.get_response(request)
        return response
    
    def get_user_ip(self, request):
        """این تابع فقط وقتی صدا زده میشه که واقعا نیاز باشه"""
        if not request.user.is_authenticated:
            return None
        
        ip = self.get_client_ip(request)
        if not ip:
            return None
        
        try:
            ip_address, created = IpAddress.objects.get_or_create(ips=ip)
            # اگر می‌خواهید کاربر رو هم آپدیت کنید
            if hasattr(request.user, 'ip_address'):
                request.user.ip_address = ip_address
            return ip_address
        except Exception:
            return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')