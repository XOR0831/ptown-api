from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Amenities, Services, OperationHours, Comments, Barbershop, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email"
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password"
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField(allow_blank=True, allow_null=True)
    email = serializers.EmailField(allow_blank=True, allow_null=True)
    password = serializers.CharField(allow_blank=True, allow_null=True)
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password"
        ]


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = "__all__"


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"


class OperationHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationHours
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class BarbershopSerializer(serializers.ModelSerializer):
    amenities = AmenitiesSerializer(many=True, required=False)
    services = ServicesSerializer(many=True, required=False)
    hours = OperationHoursSerializer(many=True, required=False)
    comments = CommentsSerializer(many=True, required=False)
    favorites = UserSerializer(many=True, required=False)

    class Meta:
        model = Barbershop
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    user =  UserSerializer()
    barbershop = BarbershopSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = "__all__"