from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Amenities, Appointment, Message, Services, OperationHours, Comments, Barbershop, Profile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['id'] = self.user.id
        return data



class UserFavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id"
        ]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
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

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.set_password(validated_data["password"])
        return user
    

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
    name = serializers.CharField(validators=[])
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
    user = UserListSerializer(read_only=True)
    class Meta:
        model = Comments
        fields = "__all__"
        
        
class AppointmentFilteredListUserSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(user=self.context['request'].user)
        return super(AppointmentFilteredListUserSerializer, self).to_representation(data)

    
class AppointmentsFilteredSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = "__all__"
        list_serializer_class = AppointmentFilteredListUserSerializer
        

class AppointmentsSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, data):
        user =  self.context['request'].user
        if Appointment.objects.filter(
            Q(date=data["date"], time=data["time"]) |
            Q(date=data["date"], user=user)
        ).exists():
            raise serializers.ValidationError("There is an existing appointment")
        return data
        

class AppointmentIDSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Appointment
        fields = [
            "id"
        ]


class MessagesUserSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField()
    class Meta:
        model = Message
        fields = [
            "user"
        ]


class MessagesCreateSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField()
    class Meta:
        model = Message
        fields = [
            "origin",
            "text",
            "user"
        ]

    def create(self, data):
        user = User.objects.get(pk=data["user"])
        instance = Message.objects.create(
            user=user,
            text=data["text"],
            origin=data["origin"]
        )

        return instance


class MessagesListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    class Meta:
        model = Message
        fields = "__all__"


class BarbershopSerializer(serializers.ModelSerializer):
    amenities = AmenitiesSerializer(many=True)
    services = ServicesSerializer(many=True)
    hours = OperationHoursSerializer(many=True)
    comments = CommentsSerializer(many=True)
    favorites = UserListSerializer(many=True)
    appointments = AppointmentsSerializer(many=True)
    messages = MessagesListSerializer(many=True)

    class Meta:
        model = Barbershop
        fields = "__all__"


class BarbershopProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
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
    favorites = UserListSerializer(many=True)
    appointments = AppointmentsSerializer(many=True)
    messages = MessagesListSerializer(many=True)

    class Meta:
        model = Barbershop
        fields = "__all__"
        
 
class BarbershopListUserSerializer(serializers.ModelSerializer):
    amenities = AmenitiesSerializer(many=True)
    services = ServicesSerializer(many=True)
    hours = OperationHoursSerializer(many=True)
    comments = CommentsSerializer(many=True)
    favorites = UserListSerializer(many=True)
    appointments = AppointmentsFilteredSerializer(many=True)
    messages = MessagesListSerializer(many=True)

    class Meta:
        model = Barbershop
        fields = "__all__"


class BarbershopUpdateSerializer(serializers.ModelSerializer):
    amenities = AmenitiesSerializer(many=True, required=False)
    services = ServicesSerializer(many=True, required=False)
    hours = OperationHoursSerializer(many=True, required=False)
    comments = CommentsSerializer(many=True, required=False)
    favorites = UserFavoritesSerializer(many=True, required=False)

    class Meta:
        model = Barbershop
        fields = "__all__"

    def save(self):
        amenities_data = self.validated_data.get('amenities')
        services_data = self.validated_data.get('services')
        hours_data = self.validated_data.get('hours')
        comments_data = self.validated_data.get('comments')
        if amenities_data:
            for amenities_item in amenities_data:
                if amenities_item.get("name"):
                    if Amenities.objects.filter(name=amenities_item.get("name")).exists():
                        amenity = Amenities.objects.get(name=amenities_item.get("name"))
                    else:
                        amenity = Amenities.objects.create(**amenities_item)
                    self.instance.amenities.add(amenity)
        if services_data:
            for services_item in services_data:
                if services_item.get("name") and services_item.get("price"):
                    if Services.objects.filter(name=services_item.get("name"), price=services_item.get("price")).exists():
                        service = Services.objects.get(name=services_item.get("name"), price=services_item.get("price"))
                    else:
                        service = Services.objects.create(**services_item)
                    self.instance.services.add(service)
        if hours_data:
            for hours_item in hours_data:
                if hours_item.get("day") and hours_item.get("opening_time") and hours_item.get("closing_time"):
                    if OperationHours.objects.filter(day=hours_item.get("day"), opening_time=hours_item.get("opening_time"), closing_time=hours_item.get("closing_time")).exists():
                        hour = OperationHours.objects.get(day=hours_item.get("day"), opening_time=hours_item.get("opening_time"), closing_time=hours_item.get("closing_time"))
                    else:
                        hour = OperationHours.objects.create(**hours_item)
                    self.instance.hours.add(hour)
        if comments_data: 
            for comments_item in comments_data:
                if comments_item.get("text") and comments_item.get("rating") and comments_item.get("type"):
                    user =  self.context['request'].user
                    if Comments.objects.filter(text=comments_item.get("text"), rating=comments_item.get("rating"), type=comments_item.get("type"), user=user).exists():
                        comment = Comments.objects.get(text=comments_item.get("text"), rating=comments_item.get("rating"), type=comments_item.get("type"), user=user)
                    else:
                        comment = Comments.objects.create(
                            text=comments_item.get("text"), 
                            rating=comments_item.get("rating"), 
                            type=comments_item.get("type"),
                            user=user
                        )
                    self.instance.comments.add(comment)

                    comments = self.instance.comments.all()

                    tally = 0
                    count = 1
                    for comment in comments:
                        tally += comment.rating
                        count += 1
                    self.instance.rating = round(tally / count, 2)
        self.instance.save()
        return self.instance


class ProfileSerializer(serializers.ModelSerializer):
    user =  UserListSerializer()
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
        users_data = self.validated_data.get('user')
        if users_data:
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
