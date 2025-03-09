from django.urls import path
from . import views

urlpatterns = [
    path('get_user_data', views.get_user_data, name='index'),
]