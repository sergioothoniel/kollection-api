from rest_framework import generics

from .serializers import WorkSerializer
from .models import Work


class WorksViews(generics.ListCreateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
