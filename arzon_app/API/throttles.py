from rest_framework.throttling import UserRateThrottle
from data.data import KEY, KEY_VERCEL

# Belgilangan Baerer code bilan kelgan so;rovlar uchun throttle ishlatmasligini uchun Custom Throttle yozildi
class CustomBearerTokenRateThrottle(UserRateThrottle):
    rate = '10/day'  

    def allow_request(self, request, view):

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if auth_header.startswith('Bearer '):
            bearer_token = auth_header[len('Bearer '):].strip()
            if self.validate_token(bearer_token):
                return True
        
        return super().allow_request(request, view)

    def validate_token(self, bearer_token):
        if bearer_token == KEY or bearer_token == KEY_VERCEL:
            return True

        return False