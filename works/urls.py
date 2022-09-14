from django.urls import path

from . import views

urlpatterns = [
    path("works/<str:work_id>/", views.WorkDetailsView.as_view(), name="work_detail"),
    path("works/", views.WorksViews.as_view(), name="works"),
]
