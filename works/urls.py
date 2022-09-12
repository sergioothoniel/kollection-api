from django.urls import path
from . import views

urlpatterns = [
    path("", views.WorksViews, name="works"),
    path("/<work_id>", views.WorkDetailsView),
]
