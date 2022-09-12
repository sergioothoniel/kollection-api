from django.urls import path

from . import views

urlpatterns = [
    path("", views.WorksViews.as_view(), name="works"),
    path("<str:work_id>/", views.WorkDetailsView.as_view()),
]
