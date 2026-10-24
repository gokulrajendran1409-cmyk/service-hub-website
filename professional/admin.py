from django.contrib import admin
from .models import proreg

# Register your models here.
@admin.register(proreg)
class ProregAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'experience', 'service_charge', 'phone', 'status')
    list_filter = ('status', 'category')
    search_fields = ('name', 'email', 'phone', 'location')