from rest_framework_simplejwt.tokens import RefreshToken

def create_jwt(user_id):
    refresh = RefreshToken.for_user(user_id)
    access_token = str(refresh.access_token)  # Access token to be returned
    refresh_token = str(refresh)  # Refresh token (can be stored securely in the back-end or front-end)
    
    # Return the token to the API call
    return {
        'access': access_token,
        'refresh': refresh_token,
        'user_id': user_id  # Include the user ID (or other details) in the response
    }