from rest_framework import serializers
from .models import Medico, Ubs, Endereco

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'

class UbsSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()
    medicos = MedicoSerializer(many=True)

    class Meta:
        model = Ubs
        fields = '__all__'