from django.urls import path

from api.views.auth import register, verify
from api.views.users import get_user, delete_user_data
from api.views.sessions import (
	start_session,
	end_session,
	check_in,
	missed_check_in
)

urlpatterns = [
	#Auth
	path('auth/register/', register, name='register'),
	path('auth/verify/',verify, name='verify'),
	# path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	# path("auth/token/dummy-jwt/", views.createDummyJwt, name="dummy-jwt"),
	
    # Users
    path('user/', get_user, name='get_user_data'),
	path('user/delete/', delete_user_data, name='delete_user_data'),
	
    # Sessions
    path('session/start/', start_session, name='start_session'),
	path('session/end/', end_session, name='end_session'),
	path('session/check_in/', check_in, name='check_in'),
	path('session/miss_check_in/', missed_check_in, name='miss_check_in'),
    
    # insert happens when register happens, so we can just call create_user_data in the register view and not have an endpoint for it.
    # path('insert_user_data', views.insert_user_data, name='index'),
    # path('create_user_data', views.create_user_data, name='index'),
    
    # path('insert_user_verification_number', views.insert_user_verification_number, name='index'),
    
    # JWT Authentication
    # path('', Home.as_view()),
]