# ======= FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) =======

# test_users.py
# Module responsible for executing User and CRUD tests
# 7 tests

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
# Validates the happy path of creating a new user via POST, ensuring 
# a 201 status code (created) and the integrity of the expected contract.

def test_create_user_successfully(user_url, valid_user_payload):
    payload = valid_user_payload   
    response = requests.post(user_url, json=payload)
    response_body = response.json()

    assert response.status_code == 201
    assert response_body["message"] == "Cadastro realizado com sucesso"
    
    # Contract Validation (Schema)
    validate(instance=response_body, schema=create_user_success_schema)

    # Teardown to delete the newly created user and keep the database clean
    user_id = response_body["_id"]
    requests.delete(f"{user_url}/{user_id}")

# ====================================================================

# test_create_user_duplicated_email (POST - 400)
# Tests the business rule restriction for unique emails. Validates that the 
# system returns 400 when trying to register a user with an existing email.

def test_create_user_duplicated_email(user_url, duplicated_email_user_payload):
    # Registers the user for the first time (success: 201)
    first_response = requests.post(user_url, json=duplicated_email_user_payload)
    assert first_response.status_code == 201
    first_response_body = first_response.json()
    user_id = first_response_body["_id"]

    try:
        # Tries to register the same user for the second time (error: 400)
        response = requests.post(user_url, json=duplicated_email_user_payload)
        response_body = response.json()
        
        assert response.status_code == 400
        assert response_body["message"] == "Este email já está sendo usado"
        
        validate(instance=response_body, schema=duplicated_email_schema)
    finally:
        # Teardown: removes the registered user to clean up the database
        requests.delete(f"{user_url}/{user_id}")

# ====================================================================

# test_list_all_users (GET - 200)
# Confirms the integrity of the user listing, ensuring that the GET 
# returns 200 and that the response respects the structured list contract (schema).

def test_list_all_users(user_url):
    response = requests.get(user_url)
    response_body = response.json()

    assert response.status_code == 200
    validate(instance=response_body, schema=list_all_users_schema)

# ====================================================================

# test_delete_user_successfully_by_id (DELETE - 200 / 204)
# Validates the deletion endpoint (DELETE), confirming the successful 
# removal of the record and ensuring the user no longer exists in the database.

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
# Validates the user search endpoint by ID, confirming that 
# the record is successfully found and that the response respects 
# the expected contract.

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
# Validates the update endpoint (PUT), confirming the successful 
# update of the record and ensuring proper modification.

def test_update_user_successfully(user_url, valid_user_payload, admin_auth_headers, update_payload):
    # 1. Arrange: Create a base user
    novo_usuario = valid_user_payload.copy()
    novo_usuario["email"] = f"teste_update_{uuid.uuid4()}@qa.com.br"
    
    post_response = requests.post(user_url, json=novo_usuario)
    assert post_response.status_code == 201
    user_id = post_response.json()["_id"]

    # 2. Act: Perform the PUT request using the fixture created in conftest
    put_response = requests.put(f"{user_url}/{user_id}", json=update_payload, headers=admin_auth_headers)

    # 3. Assert
    assert put_response.status_code == 200
    assert put_response.json()["message"] == "Registro alterado com sucesso"
    
    # Teardown
    requests.delete(f"{user_url}/{user_id}")

# ====================================================================

# test_update_user_duplicated_email (PUT - 400)
# Validates the update endpoint restriction when trying to update 
# a user's email to another one that is already taken.

def test_update_user_duplicated_email(user_url, admin_auth_headers):
    # 1. Arrange: Create two distinct users
    user1 = {"nome": "User 1", "email": "user1@teste.com", "password": "123", "administrador": "true"}
    user2 = {"nome": "User 2", "email": "user2@teste.com", "password": "123", "administrador": "true"}
    
    id1 = requests.post(user_url, json=user1).json()["_id"]
    id2 = requests.post(user_url, json=user2).json()["_id"]

    # 2. Act: Try to update User 2 using User 1's email
    payload_duplicado = {"nome": "User 2", "email": "user1@teste.com", "password": "123", "administrador": "true"}
    response = requests.put(f"{user_url}/{id2}", json=payload_duplicado, headers=admin_auth_headers)
    
    # 3. Assert: Validate the error response
    assert response.status_code == 400
    assert response.json()["message"] == "Este email já está sendo usado"

    # Teardown
    requests.delete(f"{user_url}/{id1}")
    requests.delete(f"{user_url}/{id2}")

# ====================================================================