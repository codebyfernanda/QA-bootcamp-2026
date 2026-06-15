# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import pytest
import requests
import uuid

# Fixture to create user
@pytest.fixture
def my_user_fixture():
    payload = {
        "nome": "Fernanda Bastos",
        "email": f"teste_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }
    response = requests.post("https://compassuol.serverest.dev/usuarios", json=payload)
    user_id = response.json()["_id"]
    yield {"payload": payload, "id": user_id}

# Fixture to create product
@pytest.fixture
def my_product_fixture(my_user_fixture):
    # Login to obtain admin token
    user_payload = my_user_fixture["payload"]
    login_payload = {
        "email": user_payload["email"],
        "password": user_payload["password"]
    }
    login_response = requests.post("https://compassuol.serverest.dev/login", json=login_payload)
    token = login_response.json()["authorization"]
    
    # Creating a product
    headers = {
        "Authorization": token
    }
    product_payload = {
        "nome": f"Logitech MX {uuid.uuid4()}",
        "preco": 470,
        "descricao": "Mouse",
        "quantidade": 381
    }
    response = requests.post("https://compassuol.serverest.dev/produtos", json=product_payload, headers=headers)
    product_id = response.json()["_id"]
    yield {"payload": product_payload, "id": product_id, "token": token}

# ===================================================================================================================================

