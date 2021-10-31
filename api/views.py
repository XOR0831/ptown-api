from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    # Barbershop
    AppointmentIDSerializer,
    AppointmentsSerializer,
    BarbershopSerializer, 
    BarbershopListSerializer,
    BarbershopListUserSerializer,
    BarbershopCreateSerializer,
    BarbershopUpdateSerializer,
    MessagesCreateSerializer,
    MessagesListSerializer,
    MessagesUserSerializer,
    # Profile
    ProfileSerializer,
    ProfileListSerializer,
    ProfileCreateSerializer,
    ProfileUpdateSerializer,
    UserFavoritesSerializer,
    # Token
    MyTokenObtainPairSerializer
)
from .models import (
    Appointment,
    Barbershop, 
    Profile
)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


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

    @extend_schema(
        description='Add Appointment', 
        methods=["POST"],
        request=AppointmentsSerializer,
        responses=BarbershopSerializer
    )
    @action(detail=True, methods=['POST'])
    def add_appointment(self, request, pk=None):
        serializer = AppointmentsSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save(user=request.user)
        barbershop = Barbershop.objects.get(pk=pk)
        barbershop.appointments.add(appointment)
        barbershop.save()
        barber = barbershop.appointments.all()
        return Response(AppointmentsSerializer(barber, many=True).data, status=status.HTTP_200_OK)

    @extend_schema(
        description='Cancel Appointment', 
        methods=["POST"],
        request=AppointmentIDSerializer,
        responses=AppointmentsSerializer
    )
    @action(detail=True, methods=['POST'])
    def cancel_appointment(self, request, pk=None):
        serializer = AppointmentIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = Appointment.objects.get(pk=serializer.validated_data.get("id"))
        barbershop = Barbershop.objects.get(pk=pk)
        if appointment in barbershop.appointments.all():
            barbershop.appointments.remove(appointment)
        barbershop.save()
        barbers = barbershop.appointments.all()
        return Response(AppointmentsSerializer(barbers, many=True).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses=AppointmentsSerializer
    )
    @action(detail=True, methods=['GET'])
    def get_appointment(self, request, pk=None):
        barbershops = Barbershop.objects.get(pk=pk).appointments.all()
        return Response(AppointmentsSerializer(barbershops, many=True).data, status=status.HTTP_200_OK)
    
    @extend_schema(
        request=None,
        responses=BarbershopListSerializer
    )
    @action(detail=False, methods=['GET'])
    def appointment_user(self, request):
        barbershops = Barbershop.objects.filter(appointments__user=request.user).distinct()
        return Response(BarbershopListUserSerializer(barbershops, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

    @extend_schema(
        description='Add Message', 
        methods=["POST"],
        request=MessagesCreateSerializer,
        responses=MessagesListSerializer
    )
    @action(detail=True, methods=['POST'])
    def add_message(self, request, pk=None):
        serializer = MessagesCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        barbershop = Barbershop.objects.get(pk=pk)
        barbershop.messages.add(message)
        barbershop.save()
        barber = barbershop.messages.filter(user=message.user).order_by("created")
        return Response(MessagesListSerializer(barber, many=True).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=MessagesUserSerializer,
        responses=MessagesListSerializer
    )
    @action(detail=True, methods=['POST'])
    def messages_thread(self, request, pk=None):
        serializer = MessagesUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(pk=serializer.validated_data.get("user"))
        messages = Barbershop.objects.get(pk=pk).messages.filter(user=user).order_by("created")
        return Response(MessagesListSerializer(messages, many=True).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses=None
    )
    @action(detail=True, methods=['GET'])
    def messages_barber(self, request, pk=None):
        data = {}
        messages = Barbershop.objects.get(pk=pk).messages.all()
        for message in messages:
            name = "{} {}".format(message.user.first_name, message.user.last_name)
            if not name in data:
                data[name] = []
            data[name].append(MessagesListSerializer(message).data)
        return Response(data, status=status.HTTP_200_OK)


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
