from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
	#Auth
	path('auth/register/', views.register, name='register'),
	path('auth/verify/', views.verify_user_verification_number, name='verify'),
	path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path("auth/token/dummy-jwt/", views.createDummyJwt, name="dummy-jwt"),
	
    # Users
    path('users/me/', views.get_user_data, name='get_user_data'),
	path('users/delete/', views.delete_user_data, name='delete_user_data'),
	
    # Sessions
    path('sessions/start/', views.start_user_session, name='start_session'),
	path('sessions/end/', views.end_user_session, name='end_session'),
	path('sessions/check_in/', views.check_user_in, name='check_in'),
	path('sessions/miss_check_in/', views.miss_user_check_in, name='miss_check_in'),
    
    # insert happens when register happens, so we can just call create_user_data in the register view and not have an endpoint for it.
    # path('insert_user_data', views.insert_user_data, name='index'),
    # path('create_user_data', views.create_user_data, name='index'),
    
    # path('insert_user_verification_number', views.insert_user_verification_number, name='index'),
    
    # JWT Authentication
    # path('', Home.as_view()),
]