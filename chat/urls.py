from django.urls import path
from . import views

urlpatterns = [
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list),
    path('api/messages/', views.message_list),
    path('api/users/<int:pk>/', views.user_list),
    path('api/users/', views.user_list),
]