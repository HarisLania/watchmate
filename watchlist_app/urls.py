from django.urls import path
from .views import *

urlpatterns = [
    path('list/', movie_list, name='movie_list'),
    path('<str:pk>/', movie_details, name='movie_details'),
]