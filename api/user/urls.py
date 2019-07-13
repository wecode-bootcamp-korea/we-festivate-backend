from django.http import HttpResponse, JsonResponse
from django.views import View 
from django.urls import path, include
from .views import UserView, LoginView, GoogleLoginView, KakaoLoginView


urlpatterns = [
    path('', UserView.as_view()),
    path('/login', LoginView.as_view()),
    path('/login/google',GoogleLoginView.as_view()),
    path('/login/kakao',KakaoLoginView.as_view())
    ]


