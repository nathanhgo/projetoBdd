from django.db import models
from rest_framework import serializers

# Create your models here.

# EXEMPLO

# class Usuario(models):
#     nome = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#     senha = models.CharField(max_length=255)
#     telefone = models.CharField(max_length=255)
#     endereco = models.CharField(max_length=255)
#     cep = models.CharField(max_length=255)
#     cidade = models.CharField(max_length=255)
#     estado = models.CharField(max_length=255)
#     pais = models.CharField(max_length=255)
#     cpf = models.CharField(max_length=255)
#     rg = models.CharField(max_length=255)
#     data_nascimento = models.DateField()

# class UsuarioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Usuario
#         fields = [
#             'nome', 'email', 'senha'
#         ]