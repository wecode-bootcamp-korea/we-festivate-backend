from django.http import HttpResponse, JsonResponse
from django.views import View 
from django.urls import path, include
from .views import UserView, LoginView


urlpatterns = [
    path('', UserView.as_view()),
    path('/login', LoginView.as_view()),
    ]


