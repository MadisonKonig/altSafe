from rest_framework_simplejwt.tokens import RefreshToken

def create_tokens(user_id: str):
    refresh = RefreshToken()
    
    refresh['user_id'] = user_id  # Include user ID in the token payload
    
    access = refresh.access_token
    access['user_id'] = user_id  # Include user ID in the access token payload
    
    return {
        'access': str(access),
        'refresh': str(refresh)
    }
