from django.urls import path

from . import views

urlpatterns = [
    path("works/", views.WorksViews.as_view(), name="works"),
]
