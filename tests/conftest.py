# ======= ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) =======

# conftest.py
# Importações de infraestrutura responsável por fornecer a URL base e a massa 
# de dados (fixtures) para os testes automatizados da API.

import requests
import pytest
import uuid

# base_url
# Centraliza e retorna a URL raiz da API ServeRest, garantindo que 
# alterações de ambiente reflitam automaticamente em todos os testes.

@pytest.fixture
def base_url():
    return "https://compassuol.serverest.dev"

# ====================================================================

# user_url
# Centraliza e retorna a URL da rota /usuarios da API ServeRest, 
# garantindo que alterações de ambiente reflitam automaticamente 
# nos testes.

@pytest.fixture
def user_url():
    return "https://compassuol.serverest.dev/usuarios"

# ====================================================================

# products_url
# Centraliza e retorna a URL da rota /produtos da API ServeRest, 
# garantindo que alterações de ambiente reflitam automaticamente 
# nos testes.

@pytest.fixture
def products_url():
    return "https://compassuol.serverest.dev/produtos"

# ====================================================================

# carts_url
# Centraliza e retorna a URL da rota /carrinhos da API ServeRest, 
# garantindo que alterações de ambiente reflitam automaticamente 
# nos testes.

@pytest.fixture
def carts_url():
    return "https://compassuol.serverest.dev/carrinhos"

# ====================================================================

# valid_user_payload ("Caminho Feliz")
# Retorna um payload de cadastro válido e completo, utilizando UUID 
# para gerar um e-mail dinâmico e evitar conflitos de dados no banco.

@pytest.fixture
def valid_user_payload():
    return {
        "nome": "Fernanda Bastos",
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }

# ====================================================================

# invalid_password_payload (Senha Inválida - Erro 401)
# Fornece uma massa de dados exclusiva para a rota /login, enviando 
# intencionalmente credenciais incorretas para validar o bloqueio de acesso.

@pytest.fixture 
def invalid_password_payload():
    return {
        "nome": "Fernanda Bastos",
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "password": "teste",
        "administrador": "true"
    }

# ====================================================================

# invalid_password_payload (Erro 401)
# Fornece uma massa de dados exclusiva para a rota /login, enviando 
# intencionalmente credenciais incorretas para validar o bloqueio de acesso.

@pytest.fixture
def invalid_password_payload(): 
    return {
        "email": "usuario_cadastrado@qa.com.br",
        "password": "senha_incorreta"
    }

# ====================================================================

# invalid_email_payload (Erro 404/401)
# Retorna um payload de login contendo um e-mail não registrado no sistema,
# permitindo testar as respostas de segurança contra enumeração de usuários.

@pytest.fixture
def invalid_email_payload(): 
    return {
        "email": "usuario_nao_cadastrado@qa.com.br",
        "password": "Teste!123"
    } 

# ====================================================================

# login_user_without_name_payload (Erro 400)
# Massa de dados estruturada para cadastro (/usuarios) omitindo propositalmente 
# a chave obrigatória "nome", visando testar a validação de campos do servidor.

@pytest.fixture 
def login_user_without_name_payload():
    return {
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }

# ====================================================================

# login_user_without_email_payload (Erro 400)
# Payload de cadastro que exclui intencionalmente a chave "email" para 
# garantir que a API acione a exceção correta (Bad Request).

@pytest.fixture
def login_user_without_email_payload(): 
    return {
        "nome": "Fernanda Bastos",
        "password": "Teste!123",
        "administrador": "true"
    }

# ====================================================================

# login_user_without_password_payload (Erro 400)
# Fornece dados incompletos de criação de usuário, sem a chave "password",
# para validar a rigidez estrutural do contrato de cadastro.

@pytest.fixture
def login_user_without_password_payload(): 
    return {
        "nome": "Fernanda Bastos",
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "administrador": "true"
    }

# ====================================================================

# login_user_without_administrator_payload (Erro 400)
# Retorna um payload de registro ausente da flag "administrador", 
# atestando que o back-end exige a definição hierárquica do usuário.

@pytest.fixture
def login_user_without_administrator_payload():
    return {
        "nome": "Fernanda Bastos",
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
    }

# ====================================================================

# duplicated_email_user_payload (Erro 400)
# Fornece dados duplicados de criação de usuário, sem a chave "password",
# para validar a rigidez estrutural do contrato de cadastro.

@pytest.fixture
def duplicated_email_user_payload():
    return {
        "nome": "Fernanda Bastos",
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }

# ====================================================================

# admin_auth_headers (Token Válido)
# Gera automaticamente um token JWT válido, criando um usuário administrador 
# temporário apenas para obter a chave de autenticação necessária para os testes. 

@pytest.fixture
def admin_auth_headers(base_url, valid_user_payload):
    # 1. Cria o usuário administrador temporário
    create_response = requests.post(f"{base_url}/usuarios", json=valid_user_payload)
    user_id = create_response.json()["_id"]

    # 2. Faz o login para pegar o token gerado pela API
    login_payload = {
        "email": valid_user_payload["email"],
        "password": valid_user_payload["password"]
    }
    login_response = requests.post(f"{base_url}/login", json=login_payload)
    token = login_response.json()["authorization"]

    # 3. Entrega os headers prontos (YIELD)
    headers = {"Authorization": token}
    yield headers

    # 4. Teardown: Deleta o usuário admin ao final
    requests.delete(f"{base_url}/usuarios/{user_id}")

# ====================================================================

# valid_product_payload
# Massa de dados estruturada para cadastro (/usuarios) omitindo propositalmente 
# a chave obrigatória "nome", visando testar a validação de campos do servidor.

@pytest.fixture 
def valid_product_payload():
    return {
        "nome": f"ProdutoTesteAutomatizado_{uuid.uuid4()}",
        "preco": 470,
        "descricao": "Produto criado para testes",
        "quantidade": 10
    }

# ====================================================================

# novo_usuario
# Massa de dados estruturada para cadastro (/usuarios) omitindo propositalmente 
# a chave obrigatória "nome", visando testar a validação de campos do servidor.

novo_usuario = {
        "nome": "Fernanda Teste Update",
        "email": f"teste_update_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }

# ====================================================================

# update_payload
# Payload utilizado no método PUT, fornecendo dados de atualização
# do usuário criado. 

@pytest.fixture
def update_payload():
    return {
        "nome": "Fernanda Atualizada", 
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br", 
        "password": "123!Teste2", 
        "administrador": "true"
    }

# ====================================================================

# payload_factory
# Payload utilizado no método PUT, fornecendo dados de atualização
# do usuário criado. 

@pytest.fixture
def payload_factory():
    # Adicione o segundo parâmetro 'quantidade' aqui
    def _criar(product_id, quantidade):
        return {
            "produtos": [
                {
                    "idProduto": product_id,
                    "quantidade": quantidade
                }
            ]
        }
    return _criar

# ====================================================================

