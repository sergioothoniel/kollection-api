from django.urls import path
from . import views

urlpatterns = [
    path('', views.InstitutionView.as_view()),
    path('<institution_id>/', views.InstitutionDetailView.as_view()),              
]