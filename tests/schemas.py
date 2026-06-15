# ======= ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) =======

# tests/schemas.py

# ====================================================================

# Schema para POST /usuarios (no caso de "caminho feliz" ou sucesso)
# Define o contrato de sucesso para a criação de usuários (POST). 
# Assegura que a API retorne a mensagem de confirmação e o ID gerado, 
# dados essenciais para o front-end validar a ação.

create_user_success_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"}
    },
    "required": ["message", "_id"]
}

# ====================================================================

# Schema para GET /usuarios/{_id} (no caso de "caminho feliz" ou sucesso)
# Valida a estrutura completa de retorno de um usuário específico (GET). 
# Garante que a interface receba os dados corretamente tipados (como a 
# restrição de strings no administrador), evitando quebras inesperadas 
# de layout.

get_user_schema = {
    "type": "object",
    "properties": {
        "nome": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
        "administrador": {
            "type": "string", 
            "enum": ["true", "false"] # Garantia que o código só vai aceitar essas duas strings
        },
        "_id": {"type": "string"}
    },
    "required": ["nome", "email", "password", "administrador", "_id"]
}

# ====================================================================

# Schema para GET /usuarios/{_id} (no caso de "caminho feliz" ou sucesso)
# Valida a estrutura completa de retorno de um usuário específico (GET). 
# Garante que a interface receba os dados corretamente tipados (como a 
# restrição de strings no administrador), evitando quebras inesperadas 
# de layout.

get_user_by_id_schema = {
    "type": "object",
    "properties": {
        "nome": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
        "administrador": {"type": "string", "enum": ["true", "false"]},
        "_id": {"type": "string"}
    },
    "required": ["nome", "email", "password", "administrador", "_id"]
}

# ====================================================================

# Schema para Login Error (401/404) e campos ausentes (400)
# Padroniza o contrato de exceção para falhas de autenticação (401/404).
# Assegura que a API devolva a chave de mensagem correta, permitindo
# exibir o feedback visual de acesso negado na UI com segurança.

login_error_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
}

# ====================================================================

# Schemas para validação de campos ausentes no Cadastro (Erro 400)
# Verifica o contrato de erro (400) quando o campo "nome" é omitido no 
# cadastro. Garante que a resposta mapeie a falha exatamente na chave 
# correspondente, ideal para sinalizar o erro diretamente no input.

missing_name_schema = {
    "type": "object",
    "properties": {"nome": {"type": "string"}},
    "required": ["nome"]
}

# ====================================================================

#Valida a estrutura de resposta (400) para a ausência de e-mail no 
# registro. Assegura que o erro retorne na chave "email", facilitando o
# tratamento de exceções e a clareza na interface do usuário.

missing_email_schema = {
    "type": "object",
    "properties": {"email": {"type": "string"}},
    "required": ["email"]
}

# ====================================================================

# Confirma o contrato de exceção focado na falta do campo de senha (400).
# Garante que a API aponte o erro na chave correta, fundamental para a
# experiência do usuário ao tentar concluir formulários de cadastro.

missing_password_schema = {
    "type": "object",
    "properties": {"password": {"type": "string"}},
    "required": ["password"]
}

# ====================================================================

# Define a estrutura de erro para a omissão da flag de administrador (400). 
# Assegura que a requisição informe com precisão o campo faltante, mantendo 
# a consistência dos contratos de tela.

missing_administrator_schema = {
    "type": "object",
    "properties": {"administrador": {"type": "string"}},
    "required": ["administrador"]
}

# ====================================================================

# Schema para POST /usuarios (no caso de "caminho feliz" ou sucesso)
# Define o contrato de sucesso para a criação de usuários (POST). 
# Assegura que a API retorne a mensagem de confirmação e o ID gerado, 
# dados essenciais para o front-end validar a ação.

create_user_success_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"}
    },
    "required": ["message", "_id"]
}

# ====================================================================

# Schema para POST /usuarios
# Define o contrato de erro para a criação de usuários (POST) com 
# email duplicado. Assegura que a API retorne a mensagem de erro.

duplicated_email_schema = { 
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
} 

# ====================================================================

# Schema para GET /usuarios (Listar todos)
# Assegura que a API retorne a quantidade de usuários e uma lista 
# com os dados completos de cada um, validando o contrato de exibição.

list_all_users_schema = {
    "type": "object",
    "properties": {
        "quantidade": {"type": "integer"},
        "usuarios": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "password": {"type": "string"},
                    "administrador": {
                        "type": "string",
                        "enum": ["true", "false"]
                    },
                    "_id": {"type": "string"}
                },
                "required": ["nome", "email", "password", "administrador", "_id"]
            }
        }
    },
    "required": ["quantidade", "usuarios"]
}

# ====================================================================

update_user_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
}

# ====================================================================

duplicated_email_update_user_schema = { 
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
} 

# ====================================================================

create_product_success_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"}
    },
    "required": ["message", "_id"]
}

# ====================================================================

missing_product_name_schema = {
    "type": "object",
    "properties": {
        "nome": {"type": "string"}
    },
    "required": ["nome"]
}

# ====================================================================

missing_product_price_schema = { 
    "type": "object",
    "properties": {
        "preco": {"type": "string"}
    },
    "required": ["preco"]
}

# ====================================================================

missing_product_description_schema = {
    "type": "object",
    "properties": {
        "descricao": {"type": "string"}
    },
    "required": ["descricao"]
}

# ====================================================================

create_product_success_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"}
    },
    "required": ["message", "_id"]
}

# ====================================================================

create_cart_successfully_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"}
    },
    "required": ["message", "_id"]
}