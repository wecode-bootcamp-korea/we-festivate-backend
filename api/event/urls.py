from django.urls import path
from . import views
from .views import EventDetailView, AllView, PriorityView, NewestView, EventTitleSearchView, RsvpView, CommentView, NewEventView, LikeView

urlpatterns = [
    path('/', views.event_test),
    path('/newest', NewestView.as_view()),
    path('/priority', PriorityView.as_view()),
    path('/all', AllView.as_view()),
    path('/title_search', EventTitleSearchView.as_view()),
    path('/detail/<int:event_id>', EventDetailView.as_view()),
    path('/detail/<int:event_id>/rsvp', RsvpView.as_view()),
    path('/detail/<int:event_id>/like', LikeView.as_view()),
    path('/detail/<int:event_id>/comment', CommentView.as_view()),
    path('/write', NewEventView.as_view()),
]

