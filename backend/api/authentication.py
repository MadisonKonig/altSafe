from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

# from bson.objectid import ObjectId
# from backend.database.client import users_collection
class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get("access_token")

        if not token:
            return None

        try:
            decoded = AccessToken(token)
            user_id = decoded.get("user_id")

            if not user_id:
                raise AuthenticationFailed("Invalid token payload")

        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

        request.user_id = user_id

        return (None, token)