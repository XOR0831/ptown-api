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
    # Barbershop
    BarbershopSerializer, 
    # Profile
    ProfileSerializer,
    ProfileListSerializer,
    ProfileCreateSerializer,
    ProfileUpdateSerializer
)
from .models import (
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
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']

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


class BarbershopViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Amenities object
    """
    queryset = Barbershop.objects.all()
    serializer_class = BarbershopSerializer


class ProfileFilter(filters.FilterSet):

    class Meta:
        model = Profile
        fields = ["user", "contact_number", "account_type"]


class ProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Amenities object
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProfileFilter
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']

    @extend_schema(
        request=ProfileCreateSerializer,
        responses={201: ProfileSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = ProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return ProfileSerializer(instance)

    @extend_schema(
        responses={200: ProfileListSerializer}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProfileListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProfileListSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ProfileUpdateSerializer,
        responses={200: ProfileSerializer}
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        response_serializer = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(response_serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save()
        return ProfileSerializer(instance)
    
    @extend_schema(
        request=ProfileUpdateSerializer,
        responses={200: ProfileSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
