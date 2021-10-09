from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import (
    # Users
    UserSerializer,
    UserListSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    # Amenities
    AmenitiesSerializer, 
    ServicesSerializer, 
    OperationHoursSerializer, 
    CommentsSerializer, 
    BarbershopSerializer, 
    ProfileSerializer
)
from .models import (
    Amenities, 
    Services, 
    OperationHours, 
    Comments, 
    Barbershop, 
    Profile
)

class UserFilter(filters.FilterSet):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


# Create your views here.
class UsersViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Amenities object
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    @extend_schema(
        request=UserCreateSerializer,
        responses={201: UserSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return UserSerializer(instance)

    @extend_schema(
        responses={200: UserListSerializer}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=UserUpdateSerializer,
        responses={200: UserSerializer}
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        response_serializer = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(response_serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save()
        return UserSerializer(instance)



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
