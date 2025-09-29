# API Documentation - Sistema de Troca de Livros

Esta documentação descreve todos os endpoints disponíveis na API do sistema de troca de livros para integração com o front-end React.

## Base URL
```
http://localhost:8000/api/
```

## Autenticação
- A API utiliza autenticação baseada em sessão do Django
- Endpoints que requerem autenticação estão marcados com 🔒
- Para autenticação, use os endpoints de login/logout

---

## 📚 **MetaBooks** - Catálogo de Livros

### Listar todos os livros
```http
GET /api/metabooks/
```
**Resposta:**
```json
{
  "result": [
    {
      "id": 1,
      "title": "O Senhor dos Anéis",
      "description": "Uma aventura épica",
      "author": "J.R.R. Tolkien",
      "pages": 1216,
      "release_date": "1954-07-29",
      "cover_url": "https://example.com/cover.jpg"
    }
  ]
}
```

### Buscar livro por ID
```http
GET /api/metabooks/{id}/
```

### Criar novo livro
```http
POST /api/metabooks/
```
**Body:**
```json
{
  "title": "Nome do Livro",
  "description": "Descrição do livro",
  "author": "Nome do Autor",
  "pages": 300,
  "release_date": "2023-01-01",
  "cover_url": "https://example.com/cover.jpg"
}
```

### Atualizar livro
```http
PATCH /api/metabooks/{id}/
```

### Deletar livro
```http
DELETE /api/metabooks/{id}/
```

### Filtrar livros
```http
GET /api/metabooks/filter/?title=senhor&author=tolkien&release_date=1954
```
**Query Parameters:**
- `title` (opcional): Filtrar por título (busca parcial)
- `author` (opcional): Filtrar por autor (busca parcial)
- `release_date` (opcional): Filtrar por data de lançamento

### Listar livros físicos de um livro específico
```http
GET /api/metabooks/{id}/physicalbooks/
```

---

## 📖 **PhysicalBooks** - Livros Físicos

### Listar todos os livros físicos
```http
GET /api/physicalbooks/
```
**Resposta:**
```json
{
  "result": [
    {
      "id": 1,
      "meta_book": 1,
      "owner": 2,
      "description": "Livro em bom estado",
      "created_at": "2023-01-15"
    }
  ]
}
```

### Buscar livro físico por ID
```http
GET /api/physicalbooks/{id}/
```

### Criar novo livro físico
```http
POST /api/physicalbooks/
```
**Body:**
```json
{
  "meta_book": 1,
  "owner": 2,
  "description": "Livro em excelente estado",
  "created_at": "2023-01-15"
}
```

### Atualizar livro físico
```http
PATCH /api/physicalbooks/{id}/
```

### Deletar livro físico
```http
DELETE /api/physicalbooks/{id}/
```

---

## 👥 **Users** - Usuários

### Listar todos os usuários
```http
GET /api/users/
```
**Resposta:**
```json
{
  "result": [
    {
      "id": 1,
      "username": "joao123",
      "first_name": "João",
      "email": "joao@email.com",
      "description": "Amante de livros"
    }
  ]
}
```

### Buscar usuário por ID
```http
GET /api/users/{id}/
```

### Criar novo usuário (Registro)
```http
POST /api/users/
```
**Body:**
```json
{
  "username": "joao123",
  "password": "senha123",
  "first_name": "João",
  "email": "joao@email.com",
  "description": "Amante de livros"
}
```

### Atualizar usuário
```http
PATCH /api/users/{id}/
```

### Deletar usuário
```http
DELETE /api/users/{id}/
```

### 🔒 Login
```http
POST /api/users/login/
```
**Body:**
```json
{
  "username": "joao123",
  "password": "senha123"
}
```
**Resposta de sucesso:**
```json
{
  "result": {
    "id": 1,
    "username": "joao123",
    "first_name": "João",
    "email": "joao@email.com",
    "description": "Amante de livros"
  }
}
```

### 🔒 Logout
```http
POST /api/users/logout/
```

### 🔒 Obter dados do usuário logado
```http
GET /api/users/me/
```

---

## 🔄 **Transactions** - Transações

### 🔒 Listar transações do usuário
```http
GET /api/transactions/
```
**Nota:** Retorna apenas transações onde o usuário é o antigo ou novo proprietário.

### 🔒 Buscar transação por ID
```http
GET /api/transactions/{id}/
```
**Nota:** Apenas se o usuário for parte da transação.

### 🔒 Criar nova transação
```http
POST /api/transactions/
```
**Body:**
```json
{
  "old_owner": 1,
  "new_owner": 2,
  "transaction_type": "troca",
  "transaction_status": "pendente"
}
```
**Nota:** O usuário logado deve ser um dos proprietários da transação.

**Resposta:**
```json
{
  "result": {
    "id": 1,
    "old_owner": 1,
    "new_owner": 2,
    "transaction_date": "2023-01-15",
    "transaction_type": "troca",
    "transaction_status": "pendente"
  }
}
```

**⚠️ Importante:** 
- Atualização e exclusão de transações não são permitidas
- Apenas usuários autenticados podem acessar transações

---

## 🔗 **Transaction_PhysicalBook** - Relação Transação-Livro

### Listar todas as relações
```http
GET /api/transaction_physicalbook/
```

### Buscar relação por ID
```http
GET /api/transaction_physicalbook/{id}/
```

### Criar nova relação
```http
POST /api/transaction_physicalbook/
```
**Body:**
```json
{
  "transaction": 1,
  "physical_book": 2
}
```

### Atualizar relação
```http
PATCH /api/transaction_physicalbook/{id}/
```

### Deletar relação
```http
DELETE /api/transaction_physicalbook/{id}/
```

---

## 📋 **Documentação Swagger**

Para uma documentação interativa completa, acesse:
```
http://localhost:8000/swagger/
```

---

## 🔧 **Configuração para Front-end React**

### Exemplo de configuração do Axios:
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  withCredentials: true, // Importante para manter a sessão
  headers: {
    'Content-Type': 'application/json',
  }
});

// Interceptor para lidar com autenticação
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirecionar para login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### Exemplo de uso:
```javascript
// Login
const login = async (username, password) => {
  const response = await api.post('/users/login/', { username, password });
  return response.data.result;
};

// Listar livros
const getBooks = async () => {
  const response = await api.get('/metabooks/');
  return response.data.result;
};

// Criar transação
const createTransaction = async (oldOwner, newOwner, type, status) => {
  const response = await api.post('/transactions/', {
    old_owner: oldOwner,
    new_owner: newOwner,
    transaction_type: type,
    transaction_status: status
  });
  return response.data.result;
};
```

---

## 📝 **Notas Importantes**

1. **Autenticação**: Use `withCredentials: true` no Axios para manter a sessão
2. **CORS**: Certifique-se de que o Django está configurado para aceitar requisições do front-end
3. **Permissões**: Alguns endpoints requerem autenticação (marcados com 🔒)
4. **Validação**: Todos os endpoints retornam erros de validação quando os dados são inválidos
5. **Respostas**: Todas as respostas seguem o padrão `{ "result": dados }`

---

## 🚀 **Como executar o projeto**

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute as migrações:
```bash
python manage.py migrate
```

3. Inicie o servidor:
```bash
python manage.py runserver
```

4. Acesse a documentação Swagger em: `http://localhost:8000/swagger/`

Para execução em desenvolvimento:
- Clone o código
- Execute "pip install -r requirements.txt"
- Execute "python .\project\manage.py runserver"
- Abra o localhost:8000