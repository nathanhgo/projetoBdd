from django.shortcuts import render

from rest_framework import viewsets, status
from .models import UserProfile, MetaBooks, PhysicalBooks, Transactions, Transaction_PhysicalBook
from .serializers import UserProfileSerializer, MetaBooksSerializer, PhysicalBooksSerializer, TransactionsSerializer, Transaction_PhysicalBookSerializer
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
    permission_classes = [AllowAny]


class PhysicalBooksViewSet(viewsets.ModelViewSet):
    queryset = PhysicalBooks.objects.all()
    serializer_class = PhysicalBooksSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        physical_books = PhysicalBooks.objects.all()
        serializer = PhysicalBooksSerializer(physical_books, many=True)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        print(request.data)
        meta_book = request.data.get('meta_book')
        meta_book = MetaBooks.objects.get(pk=meta_book)
        owner = request.data.get('owner')
        owner = UserProfile.objects.get(pk=owner)
        created_at = request.data.get('created_at')

        if meta_book and owner and created_at:
            physical_book = PhysicalBooks.objects.create(meta_book=meta_book, owner=owner, created_at=created_at)
            serializer = PhysicalBooksSerializer(physical_book)
            return Response({ 'result': serializer.data }, status=HTTP_200_OK)
        else:
            return Response({ 'result': 'Dados inválidos'}, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(PhysicalBooks, pk=pk)
        serializer = self.get_serializer(instance)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(PhysicalBooks, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)
    
    def destroy(self, request, pk, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(PhysicalBooks, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.destroy(instance)
        return Response(serializer.data)


class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
    permission_classes = [AllowAny]


class Transaction_PhysicalBookViewSet(viewsets.ModelViewSet):
    queryset = Transaction_PhysicalBook.objects.all()
    serializer_class = Transaction_PhysicalBookSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        transaction_physicalbook = Transaction_PhysicalBook.objects.all()
        serializer = Transaction_PhysicalBookSerializer(transaction_physicalbook, many=True)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        print(request.data)
        transaction = request.data.get('transaction')
        transaction = Transactions.objects.get(pk=transaction)
        physical_book = request.data.get('physical_book')
        physical_book = PhysicalBooks.objects.get(pk=physical_book)

        if transaction and physical_book:
            transaction_physicalbook = Transaction_PhysicalBook.objects.create(transaction=transaction, physical_book=physical_book)
            serializer = Transaction_PhysicalBookSerializer(transaction_physicalbook)
            return Response({ 'result': serializer.data }, status=HTTP_200_OK)
        else:
            return Response({ 'result': 'Dados inválidos'}, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(Transaction_PhysicalBook, pk=pk)
        serializer = self.get_serializer(instance)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(Transaction_PhysicalBook, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)
    
    def destroy(self, request, pk, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(Transaction_PhysicalBook, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.destroy(instance)
        return Response(serializer.data)