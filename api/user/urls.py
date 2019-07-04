from django.http import HttpResponse, JsonResponse
from django.views import View 
from django.urls import path, include
from .views import UserView

urlpatterns = [
    path('', UserView.as_view()),
    ]

