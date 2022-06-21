from django.urls import path
from .views import *

urlpatterns = [
    path('list/', MovieListView.as_view(), name='movie_list'),
    path('<str:pk>/', MovieDetailsView.as_view(), name='movie_details'),
]