from rest_framework import serializers
from .models import UserProfile, Authors, MetaBooks, PhysicalBooks, Transactions


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'email', 'description']

class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ['id', 'name']

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
        fields = ['id', 'old_owner', 'new_owner', 'physical_book', 'transaction_date', 'transaction_type']