from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import AmenitiesSerializer, ServicesSerializer, OperationHoursSerializer, CommentsSerializer, BarbershopSerializer, ProfileSerializer
from .models import Amenities, Services, OperationHours, Comments, Barbershop, Profile

# Create your views here.
class AmenitiesViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Amenities object
    """
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer


class ServicesViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Amenities object
    """
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer


class OperationHoursViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Amenities object
    """
    queryset = OperationHours.objects.all()
    serializer_class = OperationHoursSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Amenities object
    """
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class BarbershopViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Amenities object
    """
    queryset = Barbershop.objects.all()
    serializer_class = BarbershopSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Amenities object
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
