from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views
from .views import Home

urlpatterns = [
    # TODO: use RESTful API best practices
    path('get_user_data', views.get_user_data, name='index'),
    # path('insert_user_data', views.insert_user_data, name='index'),
    path('delete_user_data', views.delete_user_data, name='index'),
    path('create_user_data', views.create_user_data, name='index'),
    # path('insert_user_verification_number', views.insert_user_verification_number, name='index'),
    path('verify_user_verification_number', views.verify_user_verification_number, name='index'),
    
    # JWT Authentication
    path('', Home.as_view()),
    #TODO: the front end can use this, to refresh the token.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('end_user_session', views.end_user_session, name='index'),
    path('start_user_session', views.start_user_session, name='index'),
]