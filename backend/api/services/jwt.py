from rest_framework_simplejwt.tokens import RefreshToken
from database.getdata import *

def create_jwt(user_id):
    user = get_data(user_id)
    user_obj = MockUser(user)
    refresh = RefreshToken.for_user(user_obj)
    access_token = str(refresh.access_token)  # Access token to be returned
    refresh_token = str(refresh)  # Refresh token (can be stored securely in the back-end or front-end)
    
    # Return the token to the API call
    return {
        'access': access_token,
        'refresh': refresh_token,
        'user_id': user_id  # Include the user ID (or other details) in the response
    }

class MockUser:
    def __init__(self, user_data, is_auth = False):
        self.id = str(user_data['_id'])  # Ensure id is a string
        self.name = user_data.get('name', None)  # You can add more fields here if needed
        if is_auth is True:
            self.is_authenticated = True

    def __str__(self):
        return f"MockUser(id={self.id}, name={self.name})"