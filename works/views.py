from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import Work
from .permissions import IsWorkOwnerOrInternOrReadOnly, WorkViewPermission
from .serializers import WorkSerializer


class WorksViews(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [WorkViewPermission]

    serializer_class = WorkSerializer

    def get_queryset(self):

        works = Work.objects.all()

        if self.request.user.is_authenticated:
            queryset = [
                work_dict
                for work_dict in works
                if work_dict.users.all()[0].institution == self.request.user.institution
                or work_dict.visibility == "Public"
            ]
            return queryset
        else:
            return Work.objects.filter(visibility="Public")


class WorkDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsWorkOwnerOrInternOrReadOnly]

    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    lookup_url_kwarg = "work_id"
