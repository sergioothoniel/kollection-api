from django.urls import path

from .views import ReviewView

urlpatterns = [path("reviews/", ReviewView.as_view())]
