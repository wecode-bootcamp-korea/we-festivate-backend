from django.http import HttpResponse, JsonResponse
from django.views import View #why??
from django.urls import path, include
from . import views
from .views import testing

urlpatterns = [
    path('/', views.testing),
]

