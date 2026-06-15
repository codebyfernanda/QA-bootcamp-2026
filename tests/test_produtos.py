# ======= ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) =======

# test_produtos.py
# Módulo responsável por executar os testes de Produtos e CRUD
# Contendo 9 testes

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
# Valida o fluxo completo de cadastro de um novo produto, garantindo 
# que o retorno seja 200/201, que o contrato seja respeitado e que 
# o produto seja removido ao final do teste.

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
# Tenta criar um produto sem token de autenticação válido, 
# validando o bloqueio de acesso.

def test_create_product_without_admin_token(products_url, valid_product_payload):
    payload = valid_product_payload

    response = requests.post(products_url, json=payload)
    response_body = response.json()

    assert response.status_code in [401, 403]
    
    # CORREÇÃO 1: String atualizada para bater exatamente com a resposta da API
    assert response_body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

    validate(instance=response_body, schema=login_error_schema)

# ====================================================================

# test_create_product_without_name (POST - 400)
# Tenta cadastrar um produto sem informar o campo "nome", 
# validando o bloqueio e a mensagem de erro.

def test_create_product_without_name(products_url, admin_auth_headers, valid_product_payload):
    # Usando .copy() para não modificar a fixture original
    payload = valid_product_payload.copy()
    payload.pop("nome")
    
    response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    response_body = response.json()

    assert response.status_code == 400
    
    # Buscando a chave "nome" em vez de "message"
    assert "nome" in response_body
    assert response_body["nome"] == "nome é obrigatório"

    validate(instance=response_body, schema=missing_product_name_schema)

# ====================================================================

# test_create_product_without_price (POST - 400)
# Tenta cadastrar um produto sem informar o campo "preço", 
# validando o bloqueio e a mensagem de erro.

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
# Tenta cadastrar um produto sem informar o campo "descrição", 
# validando o bloqueio e a mensagem de erro.

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
# Valida a busca de um produto pelo ID, garantindo que o GET retorne 200
# e que o contrato seja respeitado.

def test_search_product_by_id(products_url, admin_auth_headers, valid_product_payload):
    payload = valid_product_payload.copy()

    # Cria o produto
    create_response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    assert create_response.status_code in [200, 201]

    product_id = create_response.json()["_id"]
    
    # Busca o produto
    get_response = requests.get(f"{products_url}/{product_id}")
    assert get_response.status_code == 200

    # AQUI: Se você quiser validar a busca, precisará de um get_product_schema
    # validate(instance=get_response.json(), schema=get_product_schema)

    # Teardown
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================

# test_update_product_with_token (PUT - 200)
# Valida a atualização de um produto pelo ID, garantindo que o PUT retorne 200
# e que o contrato seja respeitado.

def test_update_product_with_token(products_url, admin_auth_headers, valid_product_payload):
    payload = valid_product_payload.copy()

    # Cria o produto
    create_response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    product_id = create_response.json()["_id"]

    # Altera o nome no payload
    payload["nome"] = "Produto Atualizado Automatizado"

    # Atualiza o produto
    put_response = requests.put(f"{products_url}/{product_id}", json=payload, headers=admin_auth_headers)
    assert put_response.status_code == 200
    assert put_response.json()["message"] == "Registro alterado com sucesso"

    # Teardown
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================

# test_update_product_without_token (PUT - 401)
# Tenta atualizar um produto sem informar o campo "nome", 
# validando o bloqueio e a mensagem de erro.

def test_update_product_without_token(products_url, valid_product_payload, admin_auth_headers):
    payload = valid_product_payload.copy()
    
    # 1. Cria um produto válido (PRECISA DO TOKEN AQUI)
    create_response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    product_id = create_response.json()["_id"]

    # 2. Tenta atualizar ESSE produto específico, mas SEM mandar o header de token
    put_response = requests.put(f"{products_url}/{product_id}", json=payload)
    put_response_body = put_response.json()

    # 3. Validações
    assert put_response.status_code in [401, 403]
    assert put_response_body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"
    
    validate(instance=put_response_body, schema=login_error_schema)
    
    # Teardown
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================

# test_delete_product_successfully (DELETE - 200)
# Valida a exclusão de um produto pelo ID, garantindo que o DELETE retorne 200
# e que o contrato seja respeitado.

def test_delete_product_successfully(products_url, admin_auth_headers, valid_product_payload):
    payload = valid_product_payload.copy()

    create_response = requests.post(products_url, json=payload, headers=admin_auth_headers)
    product_id = create_response.json()["_id"]

    delete_response = requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Registro excluído com sucesso"