from django.contrib import admin
from .models import FuelPrice

# Register your models here.

class FuelAdmin(admin.ModelAdmin):
    list_display = ('truckstop_name', 'address', 'city', 'state', 'retail_price')

admin.site.register(FuelPrice, FuelAdmin)