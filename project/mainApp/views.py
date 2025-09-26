from django.shortcuts import render

from rest_framework import viewsets
from .models import UserProfile, MetaBooks, PhysicalBooks, Transactions
from .serializers import UserProfileSerializer, MetaBooksSerializer, PhysicalBooksSerializer, TransactionsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

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
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response({ 'users': serializer.data }, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        print(request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if username and email and password:
            user = UserProfile.objects.create_user(username=username, email=email, password=password)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({ 'Uma ou mais informação obrigatória não foi preenchida'}, status=400)









class MetaBooksViewSet(viewsets.ModelViewSet):
    queryset = MetaBooks.objects.all()
    serializer_class = MetaBooksSerializer

class PhysicalBooksViewSet(viewsets.ModelViewSet):
    queryset = PhysicalBooks.objects.all()
    serializer_class = PhysicalBooksSerializer

class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer

