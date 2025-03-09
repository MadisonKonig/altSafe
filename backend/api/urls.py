from django.urls import path
from . import views

urlpatters = [
    path("api/getdata", views.homeview),
]