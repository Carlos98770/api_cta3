from django.db import models
from django.contrib.auth.models import User

class Medico(models.Model):
    STATUS_CHOICES = [
        ('Presente', 'Presente'),
        ('Ausente', 'Ausente'),
    ]

    nome = models.CharField(max_length=100, unique=True)
    especialidade = models.CharField(max_length=80)
    crm = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Ausente')
    cpf = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.nome

class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.CharField(max_length=15)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"

class Ubs(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    telefone = models.CharField(max_length=100, unique=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)
    medicos = models.ManyToManyField(Medico)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
