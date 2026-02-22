from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None  # No token provided

        try:
            prefix, token = auth_header.split(" ")
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format")

        if prefix.lower() != "bearer":
            raise AuthenticationFailed("Invalid token prefix")

        try:
            decoded = AccessToken(token)
            user_id = decoded.get("user_id")

            if not user_id:
                raise AuthenticationFailed("Invalid token payload")

        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

        # Attach user_id to request
        request.user_id = user_id

        # DRF expects a tuple (user, auth)
        return (None, token)