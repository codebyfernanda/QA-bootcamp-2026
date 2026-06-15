# ======= FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) =======

# test_login.py
# Module responsible for executing Login and Authentication tests
# 7 tests

import requests
from jsonschema import validate
from tests.schemas import (
    create_user_success_schema,
    login_error_schema,
    missing_name_schema,
    missing_email_schema,
    missing_password_schema,
    missing_administrator_schema
)

# test_login_successfully (POST - 201)
# Validates the complete flow of successful user creation (POST). 
# Ensures a 201 status code response, strict contract validation (schema), 
# and performs database cleanup (teardown) at the end.

# Successfully creating a user (201)
def test_create_user_successfully(base_url, valid_user_payload):
    payload = valid_user_payload

    # Action
    response = requests.post(f"{base_url}/usuarios", json=payload)
    response_body = response.json()

    # More assertive validations, so to speak
    assert response.status_code == 201
    assert response_body["message"] == "Cadastro realizado com sucesso"
    
    # Contract Validation (Schema)
    validate(instance=response_body, schema=create_user_success_schema)

    # Teardown: Delete the newly created user to keep the database clean
    user_id = response_body["_id"]
    requests.delete(f"{base_url}/usuarios/{user_id}")

# ====================================================================

# test_login_invalid_password (POST - 401)
# Tests the authentication security layer on the /login route. 
# Ensures that the system blocks access and returns 401 with a generic 
# error message when receiving an incorrect password.

def test_login_invalid_password(base_url, invalid_password_payload):
    # Exclusive payload for login (with a non-existent email or wrong password)
    payload = invalid_password_payload

    # Action: Making the request to the /login route
    response = requests.post(f"{base_url}/login", json=payload)
    response_body = response.json()

    # Validations: Here the API must block access
    assert response.status_code == 401
    assert response_body["message"] == "Email e/ou senha inválidos"

    validate(instance=response_body, schema=login_error_schema)

# ====================================================================

# test_login_nonexistent_user (POST - 404)
# Validates login blocking for unregistered emails. Confirms 
# the appropriate error status code (401/404) and the expected message 
# to prevent unauthorized access.

def test_login_nonexistent_user(base_url, invalid_email_payload):
    # Exclusive payload for login (with a non-existent email or wrong password)
    payload = invalid_email_payload

    # Action: Making the request to the /login route
    response = requests.post(f"{base_url}/login", json=payload)
    response_body = response.json()

    # Validations: Here the API must block access
    assert response.status_code in [401, 404]
    assert response_body["message"] in ["Usuário não encontrado", "Email e/ou senha inválidos"]

    validate(instance=response_body, schema=login_error_schema)

# ====================================================================

# test_login_without_name (POST - 400)
# Verifies the requirement of the "nome" field on the registration route (/usuarios). 
# Ensures that the API rejects the request with a 400 status and specifically 
# indicates the missing key.

def test_login_without_name(base_url, login_user_without_name_payload):
    # Payload for user creation, intentionally missing the "nome" key
    payload = login_user_without_name_payload

    # Action: Making the request to the REGISTRATION route (/usuarios)
    response = requests.post(f"{base_url}/usuarios", json=payload)
    response_body = response.json()

    # Validations: The API returns 400 and indicates that the "nome" field was missing
    assert response.status_code == 400
    
    # Instead of "message", we look for the "nome" key
    assert "nome" in response_body
    assert response_body["nome"] == "nome é obrigatório"

    validate(instance=response_body, schema=missing_name_schema)

# ====================================================================

# test_login_without_email (POST - 400)
# Validates the business rule that requires the "email" field in user creation. 
# Confirms the restriction (status 400) and the error message linked exactly 
# to the absence of this data.

def test_login_without_email(base_url, login_user_without_email_payload):
    payload = login_user_without_email_payload
    response = requests.post(f"{base_url}/usuarios", json=payload)
    response_body = response.json()

    assert response.status_code == 400
    assert "email" in response_body
    assert response_body["email"] == "email é obrigatório"

    validate(instance=response_body, schema=missing_email_schema)

# ====================================================================

# test_login_without_password (POST - 400)
# Tests the structural constraint ensuring that "password" is indispensable in the
# registration payload. Ensures a 400 return with the alert focused on the 
# password field.

def test_login_without_password(base_url, login_user_without_password_payload):
    payload = login_user_without_password_payload
    response = requests.post(f"{base_url}/usuarios", json=payload)
    response_body = response.json()

    assert response.status_code == 400
    assert "password" in response_body
    assert response_body["password"] == "password é obrigatório"

    validate(instance=response_body, schema=missing_password_schema)

# ====================================================================

# test_login_without_administrator (POST - 400) 
# Confirms that the "administrador" flag cannot be omitted in the creation request. 
# Validates the 400 status and the clarity of the API response when pointing out 
# the error in the corresponding field.

def test_login_without_administrator(base_url, login_user_without_administrator_payload): 
    payload = login_user_without_administrator_payload
    response = requests.post(f"{base_url}/usuarios", json=payload)
    response_body = response.json()

    assert response.status_code == 400
    assert "administrador" in response_body
    assert response_body["administrador"] == "administrador é obrigatório"

    validate(instance=response_body, schema=missing_administrator_schema)

# ====================================================================