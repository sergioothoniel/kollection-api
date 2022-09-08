from rest_framework import generics

# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import SerializerUsers, SerializerLoginJwt
from .models import User


class UsersViews(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = SerializerUsers


class LoginJwtView(TokenObtainPairView):
    serializer_class = SerializerLoginJwt
