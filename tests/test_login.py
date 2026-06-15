# ======= ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) =======

# test_login.py
# Módulo responsável por executar os testes de Login e Autenticação
# Contendo 7 testes

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
# Valida o fluxo completo de criação de usuário com sucesso (POST). 
# Garante o retorno de status 201, a validação estrita do contrato (schema) 
# e realiza a limpeza (teardown) do banco ao final.

# Criando usuário com sucesso (201)
def test_create_user_successfully(base_url, valid_user_payload):
    payload = valid_user_payload

    # Ação
    response = requests.post(f"{base_url}/usuarios", json=payload)
    response_body = response.json()

    # Validações mais assertivas, por assim dizer
    assert response.status_code == 201
    assert response_body["message"] == "Cadastro realizado com sucesso"
    
    # Validação de Contrato (Schema)
    validate(instance=response_body, schema=create_user_success_schema)

    # Teardown: Excluir o usuário recém-criado para não sujar o banco
    user_id = response_body["_id"]
    requests.delete(f"{base_url}/usuarios/{user_id}")

# ====================================================================

# test_login_invalid_password (POST - 401)
# Testa a camada de segurança da autenticação na rota /login. 
# Garante que o sistema barre o acesso e retorne 401 com mensagem 
# de erro genérica ao receber uma senha incorreta.

def test_login_invalid_password(base_url, invalid_password_payload):
    # Payload exclusivo para login (com um e-mail que não existe ou senha errada)
    payload = invalid_password_payload

    # Ação: Fazendo a requisição para a rota /login
    response = requests.post(f"{base_url}/login", json=payload)
    response_body = response.json()

    # Validações: Aqui sim a API deve barrar o acesso
    assert response.status_code == 401
    assert response_body["message"] == "Email e/ou senha inválidos"

    validate(instance=response_body, schema=login_error_schema)

# ====================================================================

# test_login_nonexistent_user (POST - 404)
# Valida o bloqueio de login para e-mails não cadastrados. Confirma 
# o retorno de status de erro adequado (401/404) e a mensagem esperada 
# para impedir acesso indevido.

def test_login_nonexistent_user(base_url, invalid_email_payload):
    # Payload exclusivo para login (com um e-mail que não existe ou senha errada)
    payload = invalid_email_payload

    # Ação: Fazendo a requisição para a rota /login
    response = requests.post(f"{base_url}/login", json=payload)
    response_body = response.json()

    # Validações: Aqui sim a API deve barrar o acesso
    assert response.status_code in [401, 404]
    assert response_body["message"] in ["Usuário não encontrado", "Email e/ou senha inválidos"]

    validate(instance=response_body, schema=login_error_schema)

# ====================================================================

# test_login_without_name (POST - 400)
# Verifica a obrigatoriedade do campo "nome" na rota de cadastro (/usuarios). 
# Garante que a API recusa a requisição com status 400 e indica especificamente 
# a chave faltante.

def test_login_without_name(base_url, login_user_without_name_payload):
    # Payload para criação de usuário, mas de propósito sem a chave "nome"
    payload = login_user_without_name_payload

    # Ação: Fazendo a requisição para a rota de CADASTRO (/usuarios)
    response = requests.post(f"{base_url}/usuarios", json=payload)
    response_body = response.json()

    # Validações: A API retorna 400 e indica que o campo "nome" faltou
    assert response.status_code == 400
    
    # Em vez de "message", buscamos a chave "nome"
    assert "nome" in response_body
    assert response_body["nome"] == "nome é obrigatório"

    validate(instance=response_body, schema=missing_name_schema)

# ====================================================================

# test_login_without_email (POST - 400)
#  Valida a regra de negócio que exige o campo "email" na criação de usuário. 
# Confirma o bloqueio (status 400) e a mensagem de erro vinculada exatamente 
# à ausência desse dado.

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
# Testa a restrição estrutural garantindo que a "password" é indispensável no
# payload de cadastro. Assegura o retorno 400 com o alerta focado no campo 
# da senha.

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
# Confirma que a flag "administrador" não pode ser omitida na requisição de criação. 
# Valida o status 400 e a clareza da resposta da API ao apontar o erro no campo 
# correspondente.

def test_login_without_administrator(base_url, login_user_without_administrator_payload): 
    payload = login_user_without_administrator_payload
    response = requests.post(f"{base_url}/usuarios", json=payload)
    response_body = response.json()

    assert response.status_code == 400
    assert "administrador" in response_body
    assert response_body["administrador"] == "administrador é obrigatório"

    validate(instance=response_body, schema=missing_administrator_schema)

# ====================================================================