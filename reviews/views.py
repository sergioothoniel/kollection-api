from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import Response, status

from .models import Review
from .permissions import ReviewUpdateDestroyPermission, ReviewViewPermission
from .serializers import ReviewSerializer


class ReviewView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.queryset.order_by("created_at")


class ReviewDetailView(generics.CreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewViewPermission]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewUpdateDestroyPermission]
    lookup_url_kwarg = "review_id"

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def delete(self, request, *args, **kwargs):
        review = get_object_or_404(Review, id=kwargs["review_id"])

        if len(review.works.reviews.all()) > 1:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        review.works.is_reviewed = False
        review.works.save()
        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
