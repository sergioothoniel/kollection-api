from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters

from works.filters import WorkFilter

from .models import Work
from .permissions import IsWorkOwnerOrInternOrReadOnly, WorkViewPermission
from .serializers import WorkSerializer


class WorksViews(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [WorkViewPermission]

    serializer_class = WorkSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = WorkFilter

    def get_queryset(self):

        works = Work.objects.all()

        if self.request.user.is_authenticated:
                     
            queryset = [
                work.id
                for work in works
                if work.users.all()[0].institution == self.request.user.institution
                or work.visibility == "Public"
            ]           

            return Work.objects.filter(pk__in=queryset)

        else:
            return Work.objects.filter(visibility="Public")


class WorkDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsWorkOwnerOrInternOrReadOnly]

    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    lookup_url_kwarg = "work_id"
