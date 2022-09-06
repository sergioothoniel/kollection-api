from rest_framework.views import APIView, Request, Response, status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from institutions.models import Institution

from institutions.serializers import InstitutionCreateUpdateSerializer, InstitutionSerializer


class InstitutionView(APIView):
    def post(self, request: Request):
        serializer = InstitutionCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
        

    def get(self, request):
        institutions = Institution.objects.all()

        serializer = InstitutionSerializer(institutions, many=True)        

        return Response(serializer.data)



# class InstitutionRetrieveDeleteView(generics.RetrieveDestroyAPIView):
#     queryset = Institution.objects.all()
#     serializer_class = InstitutionSerializer
#     lookup_url_kwarg = 'institution_id'



class InstitutionDetailView(APIView):
    def patch(self, request: Request, institution_id):
        institution = get_object_or_404(Institution, id=institution_id)

        serializer = InstitutionCreateUpdateSerializer(institution, request.data, partial=True)
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



