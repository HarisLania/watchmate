from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.views import WatchListOrderingFilter
from .views import *

router = DefaultRouter()
router.register('stream', StreamPlatformView, basename='stream')

urlpatterns = [
    path('watch/', WatchListView.as_view(), name='watch_list'),
    path('watch/search/', WatchListFilter.as_view(), name='watch_list_search'),   
    path('watch/order/', WatchListOrderingFilter.as_view(), name='watch_list_order'),   
    path('watch/<str:pk>/', WatchListDetailsView.as_view(), name='watch_details'),
    path('', include(router.urls)),
    # path('stream/', StreamPlatformView.as_view(), name='stream_list'),
    # path('stream/<str:pk>/', StreamPlatformDetailsView.as_view(), name='stream_details'),
    path('watch/<str:pk>/review/create/', ReviewCreate.as_view(), name='reviews_create'),
    path('watch/<str:pk>/reviews/', ReviewList.as_view(), name='reviews_list'),
    path('watch/review/<str:pk>/', ReviewDetail.as_view(), name='reviews_details'),
]