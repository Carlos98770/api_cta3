from rest_framework import serializers
from .models import Medico, Ubs

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'

class UbsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubs
        fields = '__all__'