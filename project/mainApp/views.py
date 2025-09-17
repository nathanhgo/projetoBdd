from django.shortcuts import render

from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer

def home(request):

    return render(request, 'home.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer