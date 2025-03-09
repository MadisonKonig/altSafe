from django.urls import path

from . import views

urlpatterns = [
    # This URL Path will currently trigger the task and start using TWILIO 1ce per minute!! SO PLEASE DONT USE UNLESS TESTING :( 
    path("", views.index, name="index"), # /notify/"" 
]