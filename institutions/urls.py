from django.urls import path
from . import views

urlpatterns = [
    path("institutions/", views.InstitutionView.as_view(), name="institutions"),
    path(
        "institutions/<institution_id>/",
        views.InstitutionDetailView.as_view(),
        name="institutions_id",
    ),
]
