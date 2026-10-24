from django.contrib import admin
from .models import userreg,category,Booking

# Register your models here.
admin.site.register(userreg)
admin.site.register(category)
admin.site.register(Booking)