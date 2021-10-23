from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    # Barbershop
    BarbershopSerializer, 
    BarbershopListSerializer,
    BarbershopCreateSerializer,
    BarbershopUpdateSerializer,
    # Profile
    ProfileSerializer,
    ProfileListSerializer,
    ProfileCreateSerializer,
    ProfileUpdateSerializer,
    UserFavoritesSerializer
)
from .models import (
    Barbershop, 
    Profile
)


class BarbershopFilter(filters.FilterSet):

    class Meta:
        model = Barbershop
        fields = ["name", "address", "rating"]


class BarbershopViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Amenities object
    """
    queryset = Barbershop.objects.all()
    serializer_class = BarbershopSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BarbershopFilter
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']

    @extend_schema(
        request=BarbershopCreateSerializer,
        responses={201: BarbershopSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = BarbershopCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return BarbershopSerializer(instance)

    @extend_schema(
        responses={200: BarbershopListSerializer}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BarbershopListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BarbershopListSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=BarbershopUpdateSerializer,
        responses={200: BarbershopSerializer}
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BarbershopUpdateSerializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        response_serializer = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(response_serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save()
        return BarbershopSerializer(instance)
    
    @extend_schema(
        request=BarbershopUpdateSerializer,
        responses={200: BarbershopSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        description='Add User in Favorites', 
        methods=["POST"],
        request=None,
        responses=BarbershopListSerializer
    )
    @action(detail=True, methods=['POST'])
    def add_favorite_user(self, request, pk=None):
        barbershop = Barbershop.objects.get(pk=pk)
        if request.user in barbershop.favorites.all():
            barbershop.favorites.remove(request.user)
        else:
            barbershop.favorites.add(request.user)
        barbershop.save()
        barbers = request.user.favorites.all()
        return Response(BarbershopListSerializer(barbers, many=True).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses=BarbershopListSerializer
    )
    @action(detail=False, methods=['GET'])
    def favorite_user(self, request):
        barbershops = request.user.favorites.all()
        return Response(BarbershopListSerializer(barbershops, many=True).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses=BarbershopListSerializer
    )
    @action(detail=False, methods=['GET'])
    def barbershop_of_the_month(self, request):
        barbershop = Barbershop.objects.order_by("-rating").first()
        return Response(BarbershopListSerializer(barbershop).data, status=status.HTTP_200_OK)


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
    permission_classes = [permissions.AllowAny]
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
