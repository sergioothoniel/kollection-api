from django.urls import path

from .views import ReviewDetailView, ReviewUpdateDeleteView, ReviewView

urlpatterns = [
    path("reviews/", ReviewView.as_view(), name="reviews"),
    path("reviews/<str:work_id>/", ReviewDetailView.as_view(), name="reviews_post"),
    path(
        "reviews/<str:review_id>/user/",
        ReviewUpdateDeleteView.as_view(),
        name="review_update_delete",
    ),
]
