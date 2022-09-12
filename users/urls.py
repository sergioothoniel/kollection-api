from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UsersViews.as_view(), name="users"),
    path("users/<str:user_id>/", views.UserDetailsView.as_view(), name="user_id"),
    path(
        "users/<str:user_id>/admin/",
        views.AdminDetailsView.as_view(),
        name="user_admin",
    ),
    path("login/", views.LoginView.as_view(), name="login"),
]
