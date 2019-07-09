from django.urls import path
from . import views
from .views import DetailView

urlpatterns = [
    path('/', views.event_test),
    path('/newest', views.newest),
    path('/priority', views.priority),
    path('/all/<int:start>/<int:end>', views.all),
    path('/search', views.search),
    path('/detail/<int:event_id>', DetailView.as_view()),
]

