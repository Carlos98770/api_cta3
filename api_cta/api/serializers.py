from rest_framework import serializers
from .models import Medico, Ubs, Endereco, Vinculo

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'


class MedicoComStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Medico
        fields = ['id', 'nome', 'especialidade', 'status']

    def get_status(self, obj):
        ubs = self.context.get('ubs')
        if not ubs:
            return None
        vinculo = Vinculo.objects.filter(medico=obj, ubs=ubs).first()
        return vinculo.status if vinculo else "Sem vínculo"


class UbsSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()
    medicos = serializers.SerializerMethodField()

    class Meta:
        model = Ubs
        fields = ['id', 'nome', 'telefone', 'endereco', 'medicos']

    def get_medicos(self, obj):
        medicos = obj.medicos.all()
        return MedicoComStatusSerializer(medicos, many=True, context={'ubs': obj}).data
