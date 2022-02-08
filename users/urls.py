from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, StatsView, PopularView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('stats/',StatsView.as_view()),
    path('popular/',PopularView.as_view()),
    
]