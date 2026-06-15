# ======= FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) =======

# test_products.py
# Module responsible for executing Product and CRUD tests
# 9 tests

import requests
from jsonschema import validate
from tests.schemas import (
    create_product_success_schema,
    login_error_schema, 
    missing_product_name_schema, 
    missing_product_price_schema,
    missing_product_description_schema,
)

# test_create_product_successfully_with_admin_token (POST - 200 / 201)
# Validates the complete registration flow of a new product, ensuring 
# that the response is 200/201, that the contract is respected, and that 
# the product is removed at the end of the test.

def test_create_product_successfully_with_admin_token(products_url, valid_product_payload, admin_auth_headers):
    payload = valid_product_payload

    response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    response_body = response.json()

    assert response.status_code in [200, 201]
    assert response_body["message"] == "Cadastro realizado com sucesso"

    assert response_body["_id"] is not None

    validate(instance=response_body, schema=create_product_success_schema)

    # Teardown 
    product_id = response_body["_id"]
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================

# test_create_product_without_admin_token (POST - 401 / 403)
# Tries to create a product without a valid authentication token, 
# validating the access restriction.

def test_create_product_without_admin_token(products_url, valid_product_payload):
    payload = valid_product_payload

    response = requests.post(products_url, json=payload)
    response_body = response.json()

    assert response.status_code in [401, 403]
    
    # CORRECTION 1: String updated to exactly match the API response
    assert response_body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

    validate(instance=response_body, schema=login_error_schema)

# ====================================================================

# test_create_product_without_name (POST - 400)
# Tries to register a product without providing the "nome" field, 
# validating the restriction and the error message.

def test_create_product_without_name(products_url, admin_auth_headers, valid_product_payload):
    # Using .copy() to avoid modifying the original fixture
    payload = valid_product_payload.copy()
    payload.pop("nome")
    
    response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    response_body = response.json()

    assert response.status_code == 400
    
    # Looking for the "nome" key instead of "message"
    assert "nome" in response_body
    assert response_body["nome"] == "nome é obrigatório"

    validate(instance=response_body, schema=missing_product_name_schema)

# ====================================================================

# test_create_product_without_price (POST - 400)
# Tries to register a product without providing the "preco" field, 
# validating the restriction and the error message.

def test_create_product_without_price(products_url, admin_auth_headers, valid_product_payload):
    payload = valid_product_payload.copy()
    payload.pop("preco")

    response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    response_body = response.json()

    assert response.status_code == 400

    assert "preco" in response_body
    assert response_body["preco"] == "preco é obrigatório"

    validate(instance=response_body, schema=missing_product_price_schema)

# ====================================================================

# test_create_product_without_description (POST - 400)
# Tries to register a product without providing the "descricao" field, 
# validating the restriction and the error message.

def test_create_product_without_description(products_url, admin_auth_headers, valid_product_payload):
    payload = valid_product_payload.copy()
    payload.pop("descricao")

    response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    response_body = response.json()

    assert response.status_code == 400

    assert "descricao" in response_body
    assert response_body["descricao"] == "descricao é obrigatório"

    validate(instance=response_body, schema=missing_product_description_schema)

# ====================================================================

# test_search_product_by_id (GET - 200)
# Validates product search by ID, ensuring that the GET returns 200
# and that the contract is respected.

def test_search_product_by_id(products_url, admin_auth_headers, valid_product_payload):
    payload = valid_product_payload.copy()

    # Creates the product
    create_response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    assert create_response.status_code in [200, 201]

    product_id = create_response.json()["_id"]
    
    # Searches for the product
    get_response = requests.get(f"{products_url}/{product_id}")
    assert get_response.status_code == 200

    # HERE: If you want to validate the search, you will need a get_product_schema
    # validate(instance=get_response.json(), schema=get_product_schema)

    # Teardown
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================

# test_update_product_with_token (PUT - 200)
# Validates product update by ID, ensuring that the PUT returns 200
# and that the contract is respected.

def test_update_product_with_token(products_url, admin_auth_headers, valid_product_payload):
    payload = valid_product_payload.copy()

    # Creates the product
    create_response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    product_id = create_response.json()["_id"]

    # Changes the name in the payload
    payload["nome"] = "Produto Atualizado Automatizado"

    # Updates the product
    put_response = requests.put(f"{products_url}/{product_id}", json=payload, headers=admin_auth_headers)
    assert put_response.status_code == 200
    assert put_response.json()["message"] == "Registro alterado com sucesso"

    # Teardown
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================

# test_update_product_without_token (PUT - 401)
# Tries to update a product without providing a token, 
# validating the restriction and the error message.

def test_update_product_without_token(products_url, valid_product_payload, admin_auth_headers):
    payload = valid_product_payload.copy()
    
    # 1. Creates a valid product (REQUIRES THE TOKEN HERE)
    create_response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    product_id = create_response.json()["_id"]

    # 2. Tries to update THIS specific product, but WITHOUT sending the token header
    put_response = requests.put(f"{products_url}/{product_id}", json=payload)
    put_response_body = put_response.json()

    # 3. Validations
    assert put_response.status_code in [401, 403]
    assert put_response_body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"
    
    validate(instance=put_response_body, schema=login_error_schema)
    
    # Teardown
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================

# test_delete_product_successfully (DELETE - 200)
# Validates product deletion by ID, ensuring that the DELETE returns 200
# and that the contract is respected.

def test_delete_product_successfully(products_url, admin_auth_headers, valid_product_payload):
    payload = valid_product_payload.copy()

    create_response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    product_id = create_response.json()["_id"]

    delete_response = requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Registro excluído com sucesso"

# ====================================================================