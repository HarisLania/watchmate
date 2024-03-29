from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('watchlist_app.urls')),
    path('api-auth', include('rest_framework.urls')),
    path('accounts/', include('user_app.urls')),
]
