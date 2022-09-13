from django.urls import path
from . import views

urlpatterns = [
    path("institutions/", views.InstitutionView.as_view()),
    path("institutions/<institution_id>/", views.InstitutionDetailView.as_view()),
]
