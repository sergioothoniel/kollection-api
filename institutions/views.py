from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404
from institutions.models import Institution
from rest_framework.authentication import TokenAuthentication

from institutions.permissions import InstitutionCustomPermission

from institutions.serializers import (
    InstitutionCreateUpdateSerializer,
    InstitutionSerializer,
)


class InstitutionView(APIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionCreateUpdateSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [InstitutionCustomPermission]

    def post(self, request: Request):
        serializer = InstitutionCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request):
        institutions = Institution.objects.all()

        serializer = InstitutionSerializer(institutions, many=True)

        return Response(serializer.data)


class InstitutionDetailView(APIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionCreateUpdateSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [InstitutionCustomPermission]

    def patch(self, request: Request, institution_id):
        institution = get_object_or_404(Institution, id=institution_id)

        serializer = InstitutionCreateUpdateSerializer(
            institution, request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def get(self, request, institution_id):
        institution = get_object_or_404(Institution, id=institution_id)

        serializer = InstitutionSerializer(institution)

        return Response(serializer.data)

    def delete(self, request, institution_id):
        institution = get_object_or_404(Institution, id=institution_id)

        institution.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
