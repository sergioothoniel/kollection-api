from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UsersViews.as_view(), name="users"),
    path("login/", views.LoginJwtView.as_view(), name="login"),
]
