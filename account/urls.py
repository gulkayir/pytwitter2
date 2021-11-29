from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import *
from . import views


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('refresh/', jwt_views.TokenRefreshView.as_view()),
    path('register/', RegistrationView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('reset-password/', ResetPassword.as_view()),
    path('reset-password-complete/', ResetComplete.as_view()),
    path('users/search/', views.SearchViewSet.as_view()),
    path('profile/', MyProfile.as_view()),
    path('feeds/', FeedsView.as_view()),
    path('profile/<str:username>/', ProfileView.as_view()),
    path('profile/<str:username>/followers/', GetFollowersView.as_view()),
    path('profile/<str:username>/followings/', GetFollowingsView.as_view()),
    path('follow/<str:username>/', FollowUserView.as_view()),
]
