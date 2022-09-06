from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


from .serializers import SerializerUsers
from .models import User


class UsersViews(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = SerializerUsers
