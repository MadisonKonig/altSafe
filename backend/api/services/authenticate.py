from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

# While checking the JWT Token expiry date is done automatically bysimple JWT, we want to do a user ID check.
# To do this, we create a custom JWT Authentication check
class UserAuthentication(JWTAuthentication):
    
    #Overriding JWTAuthentication's get_user method
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get("user_id")
            if user_id is None:
                raise AuthenticationFailed('User ID is missing in token.')

            # TODO: Fetch the user from the mongoDB database using the user_id
            user = {}
        except Exception as e:
            raise AuthenticationFailed(str(e))
        
        # Once user authentication is done, the user object will be accessible to all the API calls! 
        return user

        