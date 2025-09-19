from django.shortcuts import render

from rest_framework import viewsets
from .models import UserProfile, Authors, MetaBooks, PhysicalBooks, Transactions
from .serializers import UserProfileSerializer, AuthorsSerializer, MetaBooksSerializer, PhysicalBooksSerializer, TransactionsSerializer
from rest_framework.pagination import PageNumberPagination


def home(request):

    return render(request, 'home.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer


class MetaBooksViewSet(viewsets.ModelViewSet):
    queryset = MetaBooks.objects.all()
    serializer_class = MetaBooksSerializer

class PhysicalBooksViewSet(viewsets.ModelViewSet):
    queryset = PhysicalBooks.objects.all()
    serializer_class = PhysicalBooksSerializer

class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer

