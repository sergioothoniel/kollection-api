from django.urls import path

from .views import ReviewDetailView, ReviewUpdateDeleteView, ReviewView

urlpatterns = [
    path("reviews/", ReviewView.as_view()),
    path("reviews/<str:work_id>/", ReviewDetailView.as_view()),
    path("reviews/<str:review_id>/user/", ReviewUpdateDeleteView.as_view()),
]
