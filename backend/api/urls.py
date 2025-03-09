from django.urls import path
from . import views

urlpatterns = [
    path('get_user_data', views.get_user_data, name='index'),
    path('insert_user_data', views.insert_user_data, name='index'),
    path('insert_user_verified', views.insert_user_verified, name='index'),
    path('create_user_data', views.create_user_data, name='index'),
    path('insert_user_verification_number', views.insert_user_verification_number, name='index')
]