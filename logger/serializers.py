from rest_framework import serializers
from .models import ServiceLog

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLog
        fields = ['service_name', 'level', 'message', 'payload']