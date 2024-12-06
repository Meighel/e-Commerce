from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from store.models import User  

class CustomUserIDAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Fetch HTTP_X_USER_ID from request headers
        user_id = request.headers.get("HTTP_X_USER_ID")
        if not user_id:
            raise AuthenticationFailed("Missing HTTP_X_USER_ID header")
        
        try:
            # Validate if user exists in the database
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid user ID")
        
        return (user, None)  
