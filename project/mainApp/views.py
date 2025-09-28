from django.shortcuts import render

from rest_framework import viewsets
from django.contrib.auth import login, logout, authenticate
from .models import UserProfile, MetaBooks, PhysicalBooks, Transactions, Transaction_PhysicalBook
from .serializers import UserProfileSerializer, MetaBooksSerializer, PhysicalBooksSerializer, TransactionsSerializer, Transaction_PhysicalBookSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .services.google_books import search_volumes


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
    http_method_names = ['get', 'post', 'patch', 'delete']



    def list(self, request, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # O método create_user já lida com a criptografia da senha (especialmente pra parte de usuário do django)
        user = UserProfile.objects.create_user(**serializer.validated_data)
        
        # login(request, user) - ISSO VAI LOGAR O USUÁRIO

        
        return Response({'result': UserProfileSerializer(user).data}, status=HTTP_201_CREATED)

    def retrieve(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(UserProfile, pk=pk)
        serializer = self.get_serializer(instance)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(UserProfile, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)
    
    def destroy(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(UserProfile, pk=pk)
        serializer = self.get_serializer(instance)
        instance.delete()
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='login', permission_classes=[AllowAny])
    def login_user(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            serializer = UserProfileSerializer(user)
            return Response({'result': serializer.data}, status=HTTP_200_OK)
        
        return Response({'result': 'Login falhou'}, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'],  url_path='logout', permission_classes=[IsAuthenticated])
    def logout_user(self, request):
        logout(request)
        return Response({'result': 'logout bem-sucedido'}, status=HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response({'result': serializer.data}, status=HTTP_200_OK)


class MetaBooksViewSet(viewsets.ModelViewSet):
    queryset = MetaBooks.objects.all()
    serializer_class = MetaBooksSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def list(self, request, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        meta_books = MetaBooks.objects.all()
        serializer = MetaBooksSerializer(meta_books, many=True)
        return Response({'result': serializer.data}, status=HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='physicalbooks', permission_classes=[AllowAny])
    def list_physical_books(self, request, pk=None):
        get_object_or_404(MetaBooks, pk=pk)
        queryset = PhysicalBooks.objects.filter(meta_book_id=pk).select_related('meta_book', 'owner')
        serializer = PhysicalBooksSerializer(queryset, many=True)
        return Response({'result': serializer.data}, status=HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='filter', permission_classes=[AllowAny])
    def list_filter(self, request, *args, **kwargs):
        queryset = MetaBooks.objects.all()

        title = request.query_params.get('title', None)
        author = request.query_params.get('author', None)
        release_date = request.query_params.get('release_date', None)

        if title:
            queryset = queryset.filter(title__icontains=title)
        
        if author:
            queryset = queryset.filter(author__icontains=author)

        if release_date:
            queryset = queryset.filter(release_date__icontains=release_date)

        serializer = MetaBooksSerializer(queryset, many=True)
        return Response({'result': serializer.data}, status=HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='google-search', permission_classes=[AllowAny])
    def google_search(self, request):
        q = request.query_params.get('q')
        if not q:
            return Response({'result': 'Parâmetro q é obrigatório'}, status=HTTP_400_BAD_REQUEST)
        data = search_volumes(q, start=int(request.query_params.get('start', 0)),
                                limit=int(request.query_params.get('limit', 10)))
        return Response({'result': data}, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        description = request.data.get('description')
        author = request.data.get('author')
        pages = request.data.get('pages')
        release_date = request.data.get('release_date')
        cover_url = request.data.get('cover_url')
        
        if not all([title, description, author, pages, release_date]):
            return Response({'result': 'Dados inválidos'}, status=HTTP_400_BAD_REQUEST)

        obj = MetaBooks.objects.create(
            title=title,
            description=description,
            author=author,
            pages=pages,
            release_date=release_date,
            cover_url=cover_url
        )

        serializer = MetaBooksSerializer(obj)
        return Response({'result': serializer.data}, status=HTTP_201_CREATED)

    def retrieve(self, request, pk, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(MetaBooks, pk=pk)
        serializer = self.get_serializer(instance)
        return Response({'result': serializer.data}, status=HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(MetaBooks, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'result': serializer.data}, status=HTTP_200_OK)

    def destroy(self, request, pk, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        instance = get_object_or_404(MetaBooks, pk=pk)
        serializer = self.get_serializer(instance)
        instance.delete()
        return Response({'result': serializer.data}, status=HTTP_200_OK)

class PhysicalBooksViewSet(viewsets.ModelViewSet):
    queryset = PhysicalBooks.objects.all()
    serializer_class = PhysicalBooksSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def list(self, request, *args, **kwargs):
        # Regras de negócio

        # Fim de regras de negócio

        physical_books = PhysicalBooks.objects.all()
        serializer = PhysicalBooksSerializer(physical_books, many=True)
        return Response({ 'result': serializer.data }, status=HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='user-books', permission_classes=[AllowAny])
    def list_user_books(self, request, pk, *args, **kwargs):
        profile_id = pk

        if not profile_id:
            return Response(
                {'result': 'O parâmetro "profile_id" é obrigatório.'},
                status=HTTP_400_BAD_REQUEST
            )
        
        try:
            user_profile = UserProfile.objects.get(pk=profile_id)
            user_books = PhysicalBooks.objects.filter(owner=user_profile)
            serializer = PhysicalBooksSerializer(user_books, many=True)
            return Response(serializer.data, status=HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response(
                {'result': 'Nenhum perfil encontrado com o ID fornecido.'},
                status=HTTP_404_NOT_FOUND
            )

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
        return Response({'result': serializer.data}, status=HTTP_200_OK)


class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        user = request.user
        old_owner_id = request.data.get('old_owner')
        new_owner_id = request.data.get('new_owner')

        if str(user.id) not in [str(old_owner_id), str(new_owner_id)]:
            return Response({'result': 'Você deve ser um dos usuários da transação'}, status=HTTP_400_BAD_REQUEST)

        if str(old_owner_id) == str(new_owner_id):
            return Response({'result': 'Não é permitido criar transação para si mesmo'}, status=HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'result': serializer.data}, status=HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(Transactions, pk=pk)
        user = request.user

        if user != instance.old_owner and user != instance.new_owner:
            return Response({'result': 'Acesso negado'}, status=HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance)
        return Response({'result': serializer.data}, status=HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        user = request.user
        transactions = Transactions.objects.filter(old_owner=user) | Transactions.objects.filter(new_owner=user)
        serializer = self.get_serializer(transactions, many=True)
        return Response({'result': serializer.data}, status=HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='search-by-userid')
    def user_transactions(self, request, pk=None):
        user = get_object_or_404(UserProfile, pk=pk)
        # pega todas as transações em que esse user é old_owner ou new_owner
        transactions = Transactions.objects.filter(old_owner=user) or Transactions.objects.filter(new_owner=user)
        serializer = self.get_serializer(transactions, many=True)
        return Response({'result': serializer.data}, status=HTTP_200_OK)


class Transaction_PhysicalBookViewSet(viewsets.ModelViewSet):
    queryset = Transaction_PhysicalBook.objects.all()
    serializer_class = Transaction_PhysicalBookSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        user = request.user
        # só retorna Transaction_PhysicalBook ligados a transações do usuário logado
        transaction_physicalbook = Transaction_PhysicalBook.objects.filter(
            transaction__old_owner=user
        ) | Transaction_PhysicalBook.objects.filter(
            transaction__new_owner=user
        )
        serializer = self.get_serializer(transaction_physicalbook, many=True)
        return Response({'result': serializer.data}, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        transaction_id = request.data.get('transaction')
        physical_book_id = request.data.get('physical_book')

        if not transaction_id or not physical_book_id:
            return Response({'result': 'Dados inválidos'}, status=HTTP_400_BAD_REQUEST)

        transaction = get_object_or_404(Transactions, pk=transaction_id)
        physical_book = get_object_or_404(PhysicalBooks, pk=physical_book_id)

        # só pode criar se o usuário logado estiver envolvido na transação
        user = request.user
        if user != transaction.old_owner and user != transaction.new_owner:
            return Response({'result': 'Você não tem permissão para adicionar livros nesta transação'}, status=HTTP_400_BAD_REQUEST)

        obj = Transaction_PhysicalBook.objects.create(transaction=transaction, physical_book=physical_book)
        serializer = self.get_serializer(obj)
        return Response({'result': serializer.data}, status=HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(Transaction_PhysicalBook, pk=pk)
        user = request.user

        # só pode acessar se o usuário logado estiver envolvido na transação
        if user != instance.transaction.old_owner and user != instance.transaction.new_owner:
            return Response({'result': 'Acesso negado'}, status=HTTP_400_BAD_REQUEST)

        instance = get_object_or_404(Transaction_PhysicalBook, pk=pk)
        serializer = self.get_serializer(instance)
        return Response({'result': serializer.data}, status=HTTP_200_OK)


    @action(detail=True, methods=['get'], url_path='search-by-transaction')
    def list_by_transaction(self, request, pk=None):
        transaction = get_object_or_404(Transactions, pk=pk)

        # só pode ver se estiver envolvido
        user = request.user
        if user != transaction.old_owner and user != transaction.new_owner:
            return Response({'result': 'Acesso negado'}, status=HTTP_400_BAD_REQUEST)

        items = Transaction_PhysicalBook.objects.filter(transaction=transaction)
        serializer = self.get_serializer(items, many=True)
        return Response({'result': serializer.data}, status=HTTP_200_OK)
