from django.urls import path
from . import views
from .views import mypage_test, UserInfoView, MyRsvpListView, MyLikeListView

urlpatterns = [
    path('/test', views.mypage_test),
    path('/user_info', UserInfoView.as_view()),
    path('/rsvp', MyRsvpListView.as_view()),
    path('/like', MyLikeListView.as_view()),
]


