from django.urls import path

from . import views

urlpatterns = [
    path(
        "works/<str:work_id>/feedbacks/",
        views.FeedbackListCreateView.as_view(),
        name="feedback",
    ),
    path(
        "works/<str:work_id>/feedbacks/<str:feedback_id>/",
        views.FeedbackRetrieveUpdateDeleteView.as_view(),
        name="feedback_id",
    ),
]
