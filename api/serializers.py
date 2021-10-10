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
    amenities = AmenitiesSerializer(many=True)
    services = ServicesSerializer(many=True)
    hours = OperationHoursSerializer(many=True)
    comments = CommentsSerializer(many=True)
    favorites = UserSerializer(many=True)

    class Meta:
        model = Barbershop
        fields = "__all__"


class BarbershopProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbershop
        fields = [
            "id"
        ]


class BarbershopCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbershop
        fields = [
            "name",
            "description",
            "address",
            "contact_number",
            "photo",
            "rating",
            "latitude",
            "longitude",
            "verified"
        ]


class BarbershopListSerializer(serializers.ModelSerializer):
    amenities = AmenitiesSerializer(many=True)
    services = ServicesSerializer(many=True)
    hours = OperationHoursSerializer(many=True)
    comments = CommentsSerializer(many=True)
    favorites = UserSerializer(many=True)

    class Meta:
        model = Barbershop
        fields = "__all__"


class BarbershopUpdateSerializer(serializers.ModelSerializer):
    amenities = AmenitiesSerializer(many=True, required=False)
    services = ServicesSerializer(many=True, required=False)
    hours = OperationHoursSerializer(many=True, required=False)
    comments = CommentsSerializer(many=True, required=False)
    favorites = UserSerializer(many=True, required=False)

    class Meta:
        model = Barbershop
        fields = "__all__"

    def save(self, validated_data):
        amenities_data = validated_data.pop('amenities')
        services_data = validated_data.pop('services')
        hours_data = validated_data.pop('hours')
        comments_data = validated_data.pop('comments')
        for amenities_item in amenities_data:
            amenities = AmenitiesSerializer(data=amenities_item)
            amenities.is_valid(raise_exception=True)
            amenity = amenities.save()
            self.instance.amenities.add(amenity)
        for services_item in services_data:
            services = ServicesSerializer(data=services_item)
            services.is_valid(raise_exception=True)
            service = services.save()
            self.instance.services.add(service)
        for hours_item in hours_data:
            hours = OperationHoursSerializer(data=hours_item)
            hours.is_valid(raise_exception=True)
            hour = hours.save()
            self.instance.hours.add(hour)
        for comments_item in comments_data:
            comments = CommentsSerializer(data=comments_item)
            comments.is_valid(raise_exception=True)
            comment = comments.save()
            self.instance.comments.add(comment)
        self.instance.save()
        return self.instance


class ProfileSerializer(serializers.ModelSerializer):
    user =  UserSerializer()
    barbershop = BarbershopSerializer(many=True)

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileCreateSerializer(serializers.ModelSerializer):
    user =  UserCreateSerializer()
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = [
            "user",
            "contact_number",
            "photo",
            "address",
            "account_type"
        ]

    def create(self, validated_data):
        users_data = validated_data.pop('user')
        users = UserCreateSerializer(data=users_data)
        users.is_valid(raise_exception=True)
        user = users.save()
        instance = Profile.objects.create(
            user=user,
            contact_number=validated_data.get("contact_number", None),
            photo=validated_data.get("photo", None),
            address=validated_data.get("address", None),
            account_type=validated_data.get("account_type", None)
        )
        return instance



class ProfileListSerializer(serializers.ModelSerializer):
    user =  UserListSerializer()
    barbershop = BarbershopListSerializer(many=True)

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user =  UserUpdateSerializer(required=False)
    barbershop = BarbershopProfileSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = "__all__"

    def save(self):
        self.instance.contact_number = self.validated_data.get("contact_number", self.instance.contact_number)
        self.instance.photo = self.validated_data.get("photo", self.instance.photo)
        self.instance.address = self.validated_data.get("address", self.instance.address)
        self.instance.account_type = self.validated_data.get("account_type", self.instance.account_type)
        barbershops_data = self.validated_data.get('barbershop')
        if barbershops_data:
            for barbershops_item in barbershops_data:
                if Barbershop.objects.filter(id=barbershops_item["id"]).exists():
                    barbershop = Barbershop.objects.get(id=barbershops_item["id"])
                    self.instance.barbershop.add(barbershop)
        users_data = self.validated_data.pop('user')
        user = self.instance.user
        if users_data.get("first_name", None):
            user.first_name = users_data.get("first_name")
        if users_data.get("last_name", None):
            user.last_name = users_data.get("last_name")
        if users_data.get("email", None):
            user.email = users_data.get("email")
        if users_data.get("password", None):
            user.set_password(users_data.get("password"))
        user.save()
        self.instance.save()
        return self.instance