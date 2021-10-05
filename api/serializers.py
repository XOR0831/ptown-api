from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Amenities, Services, OperationHours, Comments, Barbershop, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


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
    amenities = AmenitiesSerializer(many=True)
    services = ServicesSerializer(many=True)
    hours = OperationHoursSerializer(many=True)
    comments = CommentsSerializer(many=True)
    favorites = UserSerializer(many=True)

    class Meta:
        model = Barbershop
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    user =  UserSerializer()
    barbershop = BarbershopSerializer(many=True)

    class Meta:
        model = Profile
        fields = "__all__"