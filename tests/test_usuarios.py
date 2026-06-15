# ======= ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) =======

# test_usuarios.py
# Módulo responsável por executar os testes de Usuários e CRUD
# Contendo 5 testes

import uuid 
from urllib import response 
import requests
from jsonschema import validate
from tests.schemas import (
    create_user_success_schema,
    duplicated_email_schema, 
    list_all_users_schema,
    get_user_by_id_schema, 
    update_user_schema, 
    duplicated_email_schema
    )

# test_create_user_successfully (POST - 201)
# Valida o fluxo feliz de criação de um novo usuário via POST, assegurando 
# o retorno de status 201 (criado) e a integridade do contrato esperado.

def test_create_user_successfully(user_url, valid_user_payload):
    payload = valid_user_payload   
    response = requests.post(user_url, json=payload)
    response_body = response.json()

    assert response.status_code == 201
    assert response_body["message"] == "Cadastro realizado com sucesso"
    
    # Validação de Contrato (Schema)
    validate(instance=response_body, schema=create_user_success_schema)

    # Teardown para excluir o usuário recém-criado e não "sujar" o banco
    user_id = response_body["_id"]
    requests.delete(f"{user_url}/{user_id}")

# ====================================================================

# test_create_user_duplicated_email (POST - 400)
# Testa a restrição de negócio para e-mails únicos. Valida que o sistema 
# retorna 400 ao tentar cadastrar um usuário com e-mail já existente.

def test_create_user_duplicated_email(user_url, duplicated_email_user_payload):
    # Cadastra o usuário pela primeira vez (sucesso: 201)
    first_response = requests.post(user_url, json=duplicated_email_user_payload)
    assert first_response.status_code == 201
    first_response_body = first_response.json()
    user_id = first_response_body["_id"]

    try:
        # Tenta cadastrar o mesmo usuário pela segunda vez (erro: 400)
        response = requests.post(user_url, json=duplicated_email_user_payload)
        response_body = response.json()
        
        assert response.status_code == 400
        assert response_body["message"] == "Este email já está sendo usado"
        
        validate(instance=response_body, schema=duplicated_email_schema)
    finally:
        # Teardown: remove o usuário cadastrado para limpar o banco
        requests.delete(f"{user_url}/{user_id}")

# ====================================================================

# test_list_all_users (GET - 200)
# Confirma a integridade da listagem de usuários, garantindo que o GET 
# retorne 200 e que a resposta respeite o contrato (schema) da lista estruturada.

def test_list_all_users(user_url):
    response = requests.get(user_url)
    response_body = response.json()

    assert response.status_code == 200
    validate(instance=response_body, schema=list_all_users_schema)

# ====================================================================

# test_delete_user_successfully_by_id (DELETE - 200 / 204)
# Valida o endpoint de exclusão (DELETE), confirmando a remoção do registro 
# com sucesso e garantindo que o usuário não conste mais na base de dados.

def test_delete_user_successfully_by_id(user_url, valid_user_payload):
    response = requests.post(user_url, json=valid_user_payload)
    response_body = response.json()

    assert response.status_code == 201
    
    user_id = response_body["_id"]
    requests.delete(f"{user_url}/{user_id}")
    
    response = requests.get(f"{user_url}/{user_id}")
    assert response.status_code in [200, 400]
    assert response.json()["message"] == "Usuário não encontrado"

# ====================================================================

# test_search_user_by_id (GET - 200)
# Valida o endpoint de busca de usuário por ID, confirmando que 
# o registro é encontrado com sucesso e que a resposta respeita 
# o contrato esperado.

def test_search_user_by_id(user_url, valid_user_payload):
    payload = valid_user_payload.copy()

    response = requests.post(user_url, json=payload)
    response_body = response.json()

    assert response.status_code == 201
    
    user_id = response_body["_id"]
    response = requests.get(f"{user_url}/{user_id}")
    assert response.status_code == 200

    validate(instance=response.json(), schema=get_user_by_id_schema)

# ====================================================================

# test_update_user_successfully (PUT - 200)
# Valida o endpoint de atualização (PUT), confirmando a atualização 
# do registro com sucesso e garantindo que o usuário não conste mais 
# na base de dados.

def test_update_user_successfully(user_url, valid_user_payload, admin_auth_headers, update_payload):
    # 1. Arrange: Criar um usuário base
    novo_usuario = valid_user_payload.copy()
    novo_usuario["email"] = f"teste_update_{uuid.uuid4()}@qa.com.br"
    
    post_response = requests.post(user_url, json=novo_usuario)
    assert post_response.status_code == 201
    user_id = post_response.json()["_id"]

    # 2. Act: Fazer o PUT usando a fixture que você criou no conftest
    put_response = requests.put(f"{user_url}/{user_id}", json=update_payload, headers=admin_auth_headers)

    # 3. Assert
    assert put_response.status_code == 200
    assert put_response.json()["message"] == "Registro alterado com sucesso"
    
    # Teardown
    requests.delete(f"{user_url}/{user_id}")

# ====================================================================

# test_update_user_duplicated_email (PUT - 400)
# Também valida o endpoint de atualização (PUT), confirmando a atualização 
# do registro com sucesso e garantindo que o usuário não conste mais 
# na base de dados.

def test_update_user_duplicated_email(user_url, admin_auth_headers):
    # 1. Criar dois usuários distintos
    user1 = {"nome": "User 1", "email": "user1@teste.com", "password": "123", "administrador": "true"}
    user2 = {"nome": "User 2", "email": "user2@teste.com", "password": "123", "administrador": "true"}
    
    id1 = requests.post(user_url, json=user1).json()["_id"]
    id2 = requests.post(user_url, json=user2).json()["_id"]

    # 2. Tentar atualizar o User 2 com o email do User 1
    payload_duplicado = {"nome": "User 2", "email": "user1@teste.com", "password": "123", "administrador": "true"}
    response = requests.put(f"{user_url}/{id2}", json=payload_duplicado, headers=admin_auth_headers)
    
    # 3. Validar o erro
    assert response.status_code == 400
    assert response.json()["message"] == "Este email já está sendo usado"

    # Teardown
    requests.delete(f"{user_url}/{id1}")
    requests.delete(f"{user_url}/{id2}")

# ====================================================================
