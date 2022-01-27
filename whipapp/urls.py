from django.urls import path
from .api import RegistrationAPI, LoginAPI
from knox import views as knox_views

urlpatterns = [
    path('register/', RegistrationAPI.as_view()),
    path('login/', LoginAPI.as_view()),
]