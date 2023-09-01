from rest_framework import serializers
from .models import *
from service.serializers import ServiceCompanySerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = '__all__'

class TechnicSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = Technic

class EngineSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = Engine

class TransmissionSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = Transmission

class DrivingBridgeSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = DrivingBridge

class ControlledBridgeSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = ControlledBridge

class CarSerializer(serializers.ModelSerializer):
    technic = TechnicSerializer()
    engine = EngineSerializer()
    transmission = TransmissionSerializer()
    driving_bridge = DrivingBridgeSerializer()
    controlled_bridge = ControlledBridgeSerializer()
    service_company = ServiceCompanySerializer()
    client = UserSerializer()

    class Meta:
        model = Car
        fields = '__all__'
