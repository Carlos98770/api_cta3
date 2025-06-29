from django.shortcuts import render
from .models import Medico, Ubs
from .serializers import MedicoSerializer, UbsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class MedicoList(APIView):
    def get(self, request):
        medicos = Medico.objects.all()
        serializer = MedicoSerializer(medicos, many=True)
        return Response(serializer.data)

class UbsList(APIView):
    def get(self, request):
        ubs = Ubs.objects.all()
        serializer = UbsSerializer(ubs, many=True)
        return Response(serializer.data)
    
class RegistrarPresenca(APIView):
    def post(self, request):
        cpf = request.data  # request.data é o inteiro direto, não um dicionário
        cpf_str = str(cpf).zfill(11)

        if not cpf:
            return Response({'erro': 'CPF não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            medico = Medico.objects.get(cpf=cpf_str)
        except Medico.DoesNotExist:
            return Response({'erro': 'Médico com esse CPF não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        medico.status = 'Presente'
        medico.save()

        return Response({'mensagem': f'Médico {medico.nome} marcado como Presente.'}, status=status.HTTP_200_OK)

        