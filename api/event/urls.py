from django.urls import path
from . import views
from .views import DetailView, AllView, PriorityView, NewestView, RsvpView, ReplyView

urlpatterns = [
    path('/', views.event_test),
    path('/newest', NewestView.as_view()),
    path('/priority', PriorityView.as_view()),
    path('/all', AllView.as_view()),
    path('/search', views.search),
    path('/detail/<int:event_id>', DetailView.as_view()),
    path('/detail/<int:event_id>/rsvp', RsvpView.as_view()),
    path('/detail/<int:event_id>/reply', ReplyView.as_view()),
]

