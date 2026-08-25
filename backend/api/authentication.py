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

    # def authenticate(self, request):
    #     auth_header = request.headers.get("Authorization")

    #     if not auth_header:
    #         return None  # No token provided

    #     try:
    #         prefix, token = auth_header.split(" ")
    #     except ValueError:
    #         raise AuthenticationFailed("Invalid Authorization header format")

    #     if prefix.lower() != "bearer":
    #         raise AuthenticationFailed("Invalid token prefix")

    #     try:
    #         decoded = AccessToken(token)
    #         user_id = decoded.get("user_id")

    #         if not user_id:
    #             raise AuthenticationFailed("Invalid token payload")

    #     except Exception:
    #         raise AuthenticationFailed("Invalid or expired token")

    #     # Attach user_id to request
    #     request.user_id = user_id

    #     # DRF expects a tuple (user, auth)
    #     return (None, token)

        # def authenticate(self, request):
    #     token = request.COOKIES.get("verify_token")

    #     if not token:
    #         return None

    #     try:
    #         decoded = AccessToken(token)
    #         user_id_str = decoded.get("user_id")

    #         if not user_id_str:
    #             raise AuthenticationFailed("Invalid token payload")

    #     except Exception:
    #         raise AuthenticationFailed("Invalid of expired token")

    #     try:
    #         mongo_user = users_collection.find_one({"_id": ObjectId(user_id_str)})
    #         if not mongo_user:
    #             raise AuthenticationFailed("User not found in database")
    #     except Exception:
    #         raise AuthenticationFailed("Invalid database identifier format")


    #     class AuthenticatedUser:
    #         def __init__(self, user_dict):
    #             self.id = str(user_dict["_id"])
    #             self.phone_number = user_dict.get("phone_number")
    #             self.is_verified = user_dict.get("is_verified", False)
    #             self.is_authenticated = True

    #     user_instance = AuthenticatedUser(mongo_user)

    #     request.user_id = user_instance.id

    #     return (user_instance, token)