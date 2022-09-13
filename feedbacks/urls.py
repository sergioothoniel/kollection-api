from django.urls import path
from . import views

urlpatterns = [
    path('works/<work_id>/feedbacks/', views.FeedbackListCreateView.as_view()),  
    path('works/<work_id>/feedbacks/<feedback_id>', views.FeedbackRetrieveUpdateDeleteView.as_view()),                
]