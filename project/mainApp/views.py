from django.shortcuts import render

from rest_framework import viewsets, status
from .models import UserProfile, MetaBooks, PhysicalBooks, Transactions
from .serializers import UserProfileSerializer, MetaBooksSerializer, PhysicalBooksSerializer, TransactionsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404


"""
    - CRUD com ModelViewSet
    create(): CREATE
    retrieve(): GET (um)
    update(): PUT
    partial_update(): PATCH
    destroy(): DELETE
    list(): GET (todos)
"""


def home(request):

    return render(request, 'home.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]


    def list(self, request, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        print(request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if username and email and password:
            user = UserProfile.objects.create_user(username=username, email=email, password=password)
            serializer = UserProfileSerializer(user)
            return Response({ 'result': serializer.data }, status=HTTP_200_OK)
        else:
            return Response({ 'result': 'Dados inválidos'}, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(UserProfile, pk=pk)
        serializer = self.get_serializer(instance)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(UserProfile, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)
    
    def destroy(self, request, pk, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(UserProfile, pk=pk)
        serializer = self.get_serializer(instance)
        instance.delete()
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)


class MetaBooksViewSet(viewsets.ModelViewSet):
    queryset = MetaBooks.objects.all()
    serializer_class = MetaBooksSerializer


class PhysicalBooksViewSet(viewsets.ModelViewSet):
    queryset = PhysicalBooks.objects.all()
    serializer_class = PhysicalBooksSerializer


class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
