from django.contrib import admin
from .models import TypeMaintenance, Failure, RecoveryMethod, ServiceCompany, Maintenance, Complaint
from import_export.admin import ImportExportMixin
from import_export import resources

class BaseModelAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = None
    list_display = ('id', 'name', 'description')
    list_filter = ('name',)

@admin.register(TypeMaintenance)
class TypeMaintenanceAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource
    list_display = ('id', 'name', 'description')

@admin.register(Failure)
class FailureAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource

@admin.register(RecoveryMethod)
class RecoveryMethodAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource

@admin.register(ServiceCompany)
class ServiceCompanyAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource

@admin.register(Maintenance)
class MaintenanceAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource
    list_display = ('id', 'type', 'date', 'operating_time', 'order_number', 'order_date', 'service_company', 'car')
    list_filter = ('date',)

@admin.register(Complaint)
class ComplaintsAdmin(BaseModelAdmin):
    resource_class = resources.ModelResource
    list_display = ('id', 'date_failure', 'operating_time', 'node_failure', 'date_recovery', 'downtime', 'car', 'service_company')
    list_filter = ('date_failure',)
