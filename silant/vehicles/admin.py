from django.contrib import admin
from .models import *
from import_export.admin import ImportExportMixin
from import_export import resources
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class CustomUserAdmin(UserAdmin):
    inlines = (UserInline, UserProfileInline)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class BaseModelAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = None
    list_display = ('id', 'name', 'description')
    list_filter = ('name',)

@admin.register(Technic)
class TechnicAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource

@admin.register(Engine)
class EngineAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource

@admin.register(Transmission)
class TransmissionAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource

@admin.register(DrivingBridge)
class DrivingBridgeAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource

@admin.register(ControlledBridge)
class ControlledBridgeAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource

@admin.register(Car)
class CarAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource
    list_display = (
        'id',
        'car_number',
        'technic',
        'engine',
        'transmission',
        'driving_bridge',
        'controlled_bridge',
        'date_shipment',
        'equipment',
        'client',
        'service_company',
    )
    list_filter = ('car_number',)
