from django.urls import path
from rest_framework.authtoken import views
from .views import *

urlpatterns = [
    path('login/', views.obtain_auth_token, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
]

