from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission
import os

gd_storage = GoogleDriveStorage()

permission = GoogleDriveFilePermission(
    GoogleDrivePermissionRole.READER,
    GoogleDrivePermissionType.USER,
    "kbvnxl@gmail.com"
)

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpeg','.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only .jpg (or .jpeg), and .png files are supported.')

# Create your models here.
class Amenities(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"


class Services(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"


class OperationHours(models.Model):
    day = models.CharField(max_length=255)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self) -> str:
        return self.day

    class Meta:
        verbose_name = "OperationHour"
        verbose_name_plural = "OperationHours"


class Comments(models.Model):
    text = models.TextField()
    rating = models.FloatField()
    type = models.CharField(max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default="pending")

    def __str__(self) -> str:
        return "{}: {} - {}".format(self.user.username, self.date.strftime("%A %d"), self.time.strftime("%H:%M")) 

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    origin = models.CharField(max_length=5)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self) -> str:
        return "{}: {} - {}".format(self.user.username, self.origin, self.text) 

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class Barbershop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=11, null=True, blank=True)
    photo = models.ImageField(upload_to='banners', storage=gd_storage, validators=[validate_file_extension], null=True, blank=True)
    rating = models.FloatField(default=0)
    document = models.ImageField(upload_to='documents', storage=gd_storage, validators=[validate_file_extension], null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    verified = models.BooleanField(default=False)
    amenities = models.ManyToManyField(Amenities, related_name="amenities")
    services = models.ManyToManyField(Services, related_name="services")
    hours = models.ManyToManyField(OperationHours, related_name="hours")
    comments = models.ManyToManyField(Comments, related_name="comments")
    favorites = models.ManyToManyField(User, related_name="favorites")
    appointments = models.ManyToManyField(Appointment, related_name="appointments")
    messages = models.ManyToManyField(Message, related_name="messages")

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    contact_number = models.CharField(max_length=11, null=True, blank=True)
    photo = models.ImageField(upload_to='profiles', storage=gd_storage, validators=[validate_file_extension], null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    account_type = models.CharField(max_length=5)
    barbershop = models.ManyToManyField(Barbershop, related_name="shops")

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    def get_full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
