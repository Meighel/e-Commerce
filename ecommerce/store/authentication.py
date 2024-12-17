from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class CustomUserIDAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get user ID from the request headers
        user_id = request.META.get('HTTP_X_USER_ID')
        
        if not user_id:
            raise AuthenticationFailed('User ID header missing')

        try:
            # Find the user by UUID (using the user ID passed in the header)
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            raise AuthenticationFailed('No such user')

        return (user, None)
