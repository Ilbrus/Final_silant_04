from rest_framework import serializers
from .models import *

class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = '__all__'

class ServiceCompanySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ServiceCompany

class TypeMaintenanceSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TypeMaintenance

class FailureSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Failure

class RecoveryMethodSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = RecoveryMethod

class MaintenanceSerializer(BaseSerializer):
    type = TypeMaintenanceSerializer()
    service_company = ServiceCompanySerializer()

    class Meta(BaseSerializer.Meta):
        model = Maintenance

class ComplaintSerializer(BaseSerializer):
    node_failure = FailureSerializer()
    method_recovery = RecoveryMethodSerializer()
    service_company = ServiceCompanySerializer()

    class Meta(BaseSerializer.Meta):
        model = Complaint
