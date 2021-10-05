from django.contrib import admin
from .models import Amenities, Services, OperationHours, Comments, Barbershop, Profile

# Register your models here.
admin.site.register(Amenities)
admin.site.register(Services)
admin.site.register(OperationHours)
admin.site.register(Comments)
admin.site.register(Barbershop)
admin.site.register(Profile)