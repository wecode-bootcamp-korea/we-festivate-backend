#from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('user/account',include('user.urls')),
    path('event',include('event.urls')),
    path('user', include('user.urls')),
]
