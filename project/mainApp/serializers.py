from rest_framework import serializers
from .models import UserProfile, MetaBooks, PhysicalBooks, Transactions, Transaction_PhysicalBook


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'email', 'description']

class MetaBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaBooks
        fields = ['id', 'title', 'description', 'author', 'pages', 'release_date']

class PhysicalBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalBooks
        fields = ['id', 'meta_book', 'owner', 'description', 'created_at']

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['id', 'old_owner', 'new_owner', 'transaction_date', 'transaction_type', 'transaction_status']

class Transaction_PhysicalBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_PhysicalBook
        fields = ['id', 'transaction', 'physical_book']