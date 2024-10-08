# myapp/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class URLTokenAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get token from query parameters
        token = request.query_params.get('token')
        
        if token is None:
            return None

        try:
            validated_token = self.get_validated_token(token)
            return self.get_user(validated_token), validated_token
        except AuthenticationFailed:
            return None
