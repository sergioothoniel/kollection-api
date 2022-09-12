from rest_framework import generics
from django.core import exceptions 
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer

import ipdb

from works.models import Work


class FeedbackListCreateView(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            work = get_object_or_404(Work, id=self.kwargs['work_id'])
        except exceptions.ValidationError:
            raise serializers.ValidationError({'detail':'Not a valid UUID'})
        
        return Feedback.objects.filter(work=work)


    def perform_create(self, serializer):       

        try:
            work = get_object_or_404(Work, id=self.kwargs['work_id'])
        except exceptions.ValidationError:
            raise serializers.ValidationError({'detail':'Not a valid UUID'})
        
        serializer.save(user=self.request.user, work=work)
        


class FeedbackRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedbackSerializer
    lookup_url_kwarg = 'feedback_id'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            work = get_object_or_404(Work, id=self.kwargs['work_id'])
        except exceptions.ValidationError:
            raise serializers.ValidationError({'detail':'Not a valid UUID'})
        
        return Feedback.objects.filter(work=work) 