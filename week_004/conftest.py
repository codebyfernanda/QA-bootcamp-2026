# ======= FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) =======

# conftest.py
# Infrastructure imports responsible for providing the base URL and the 
# test data (fixtures) for the automated API tests.

import requests
import pytest
import uuid

# base_url
# Centralizes and returns the root URL of the ServeRest API, ensuring that 
# environment changes automatically reflect in all tests.

@pytest.fixture
def base_url():
    return "https://compassuol.serverest.dev"

# =================================================================

# user_url
# Centralizes and returns the URL of the /usuarios route of the ServeRest API, 
# ensuring that environment changes automatically reflect in the tests.

@pytest.fixture
def user_url():
    return "https://compassuol.serverest.dev/usuarios"

# =================================================================

# products_url
# Centralizes and returns the URL of the /produtos route of the ServeRest API, 
# ensuring that environment changes automatically reflect in the tests.

@pytest.fixture
def products_url():
    return "https://compassuol.serverest.dev/produtos"

# =================================================================

# carts_url
# Centralizes and returns the URL of the /carrinhos route of the ServeRest API, 
# ensuring that environment changes automatically reflect in the tests.

@pytest.fixture
def carts_url():
    return "https://compassuol.serverest.dev/carrinhos"

# =================================================================

# valid_user_payload ("Happy Path")
# Returns a valid and complete registration payload, using UUID 
# to generate a dynamic email and avoid data conflicts in the database.

@pytest.fixture
def valid_user_payload():
    return {
        "nome": "Fernanda Bastos",
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }

# =================================================================

# invalid_password_payload (Invalid Password - Error 401)
# Provides an exclusive dataset for the /login route, intentionally 
# sending incorrect credentials to validate access restriction.

@pytest.fixture 
def invalid_password_payload():
    return {
        "nome": "Fernanda Bastos",
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "password": "teste",
        "administrador": "true"
    }

# =================================================================

# invalid_password_payload (Error 401)
# Provides an exclusive dataset for the /login route, intentionally 
# sending incorrect credentials to validate access restriction.

@pytest.fixture
def invalid_password_payload(): 
    return {
        "email": "usuario_cadastrado@qa.com.br",
        "password": "senha_incorreta"
    }

# =================================================================

# invalid_email_payload (Error 404/401)
# Returns a login payload containing an email not registered in the system,
# allowing testing of security responses against user enumeration.

@pytest.fixture
def invalid_email_payload(): 
    return {
        "email": "usuario_nao_cadastrado@qa.com.br",
        "password": "Teste!123"
    } 

# =================================================================

# login_user_without_name_payload (Error 400)
# Dataset structured for registration (/usuarios) intentionally omitting 
# the mandatory "nome" key, aiming to test server-side field validation.

@pytest.fixture 
def login_user_without_name_payload():
    return {
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }

# =================================================================

# login_user_without_email_payload (Error 400)
# Registration payload that intentionally excludes the "email" key to 
# ensure the API triggers the correct exception (Bad Request).

@pytest.fixture
def login_user_without_email_payload(): 
    return {
        "nome": "Fernanda Bastos",
        "password": "Teste!123",
        "administrador": "true"
    }

# =================================================================

# login_user_without_password_payload (Error 400)
# Provides incomplete user creation data, without the "password" key,
# to validate the structural rigidity of the registration contract.

@pytest.fixture
def login_user_without_password_payload(): 
    return {
        "nome": "Fernanda Bastos",
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "administrador": "true"
    }

# =================================================================

# login_user_without_administrator_payload (Error 400)
# Returns a registration payload missing the "administrador" flag, 
# attesting that the back-end requires the user's hierarchical definition.

@pytest.fixture
def login_user_without_administrator_payload():
    return {
        "nome": "Fernanda Bastos",
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
    }

# =================================================================

# duplicated_email_user_payload (Error 400)
# Provides data for duplicate user creation to validate the 
# structural rigidity of the registration contract.

@pytest.fixture
def duplicated_email_user_payload():
    return {
        "nome": "Fernanda Bastos",
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }

# =================================================================

# admin_auth_headers (Valid Token)
# Automatically generates a valid JWT token, creating a temporary administrator 
# user just to get the authorization key needed for the tests. 

@pytest.fixture
def admin_auth_headers(base_url, valid_user_payload):
    # 1. Creates the temporary administrator user
    create_response = requests.post(f"{base_url}/usuarios", json=valid_user_payload)
    user_id = create_response.json()["_id"]

    # 2. Logs in to get the token generated by the API
    login_payload = {
        "email": valid_user_payload["email"],
        "password": valid_user_payload["password"]
    }
    login_response = requests.post(f"{base_url}/login", json=login_payload)
    token = login_response.json()["authorization"]

    # 3. Delivers the headers (YIELD)
    headers = {"Authorization": token}
    yield headers

    # 4. Teardown: Deletes the admin user at the end
    requests.delete(f"{base_url}/usuarios/{user_id}")

# =================================================================

# valid_product_payload
# Data structure for product registration used to validate the product 
# insertion flows.

@pytest.fixture 
def valid_product_payload():
    return {
        "nome": f"ProdutoTesteAutomatizado_{uuid.uuid4()}",
        "preco": 470,
        "descricao": "Produto criado para testes",
        "quantidade": 10
    }

# =================================================================

# novo_usuario
# Data structure for testing user insertion and updates in the system.

novo_usuario = {
        "nome": "Fernanda Teste Update",
        "email": f"teste_update_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }

# =================================================================

# update_payload
# Payload used in the PUT method, providing update data for the 
# created user. 

@pytest.fixture
def update_payload():
    return {
        "nome": "Fernanda Atualizada", 
        "email": f"fernanda_{uuid.uuid4()}@qa.com.br", 
        "password": "123!Teste2", 
        "administrador": "true"
    }

# =================================================================

# payload_factory
# Factory fixture used to dynamically build cart payloads for the 
# POST /carrinhos endpoint.

@pytest.fixture
def payload_factory():
    # Add the second parameter 'quantidade' here
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

# =================================================================