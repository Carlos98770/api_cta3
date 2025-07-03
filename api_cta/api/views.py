from django.shortcuts import render
from .models import Medico, Ubs, Vinculo
from .serializers import MedicoComStatusSerializer, UbsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class MedicoList(APIView):
    def get(self, request):
        medicos = Medico.objects.all()
        serializer = MedicoComStatusSerializer(medicos, many=True)
        return Response(serializer.data)

class UbsList(APIView):
    def get(self, request):
        ubs = Ubs.objects.all()
        serializer = UbsSerializer(ubs, many=True)
        return Response(serializer.data)
    
class BuscarVinculosAPIView(APIView):
    def post(self, request):
        cpf = request.data.get("cpf")
        if not cpf:
            return Response({'erro': 'CPF não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)

        cpf_str = str(cpf).zfill(11)

        try:
            medico = Medico.objects.get(cpf=cpf_str)
        except Medico.DoesNotExist:
            return Response({'erro': 'Médico com esse CPF não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        vinculos = Vinculo.objects.filter(medico=medico).select_related('ubs__endereco')

        if not vinculos.exists():
            return Response({'erro': 'Nenhuma UBS vinculada a este médico.'}, status=status.HTTP_404_NOT_FOUND)

        ubs_list = [
            {
                "nome": vinculo.ubs.nome,
                "endereco": str(vinculo.ubs.endereco)
            }
            for vinculo in vinculos
        ]

        return Response({"ubs_vinculadas": ubs_list}, status=status.HTTP_200_OK)


class MarcarPresencaAPIView(APIView):
    def post(self, request):
        cpf = request.data.get("cpf")
        ubs_nome = request.data.get("ubs_nome")

        if not cpf or not ubs_nome:
            return Response({'erro': 'CPF e nome da UBS são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        cpf_str = str(cpf).zfill(11)

        try:
            medico = Medico.objects.get(cpf=cpf_str)
        except Medico.DoesNotExist:
            return Response({'erro': 'Médico não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            ubs = Ubs.objects.get(nome__iexact=ubs_nome)
        except Ubs.DoesNotExist:
            return Response({'erro': 'UBS com esse nome não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            vinculo = Vinculo.objects.get(medico=medico, ubs=ubs)
        except Vinculo.DoesNotExist:
            return Response({'erro': 'Médico não está vinculado a essa UBS.'}, status=status.HTTP_400_BAD_REQUEST)

        # Impede que o médico marque presença em outra UBS sem sair da anterior
        if vinculo.status == 'Ausente':
            vinculo_presente = Vinculo.objects.filter(
                medico=medico,
                status='Presente'
            ).exclude(id=vinculo.id).first()

            if vinculo_presente:
                return Response({
                    'erro': f'Médico já está presente na UBS {vinculo_presente.ubs.nome}. Saia dela antes de marcar presença em outra.'
                }, status=status.HTTP_409_CONFLICT)

            vinculo.status = 'Presente'
        else:
            vinculo.status = 'Ausente'

        vinculo.save()

        return Response({
            'mensagem': f'Médico {medico.nome} marcado como {vinculo.status} na UBS {vinculo.ubs.nome}.'
        }, status=status.HTTP_200_OK)