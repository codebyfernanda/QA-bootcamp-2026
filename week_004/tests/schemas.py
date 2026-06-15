# ======= FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) =======

# tests/schemas.py

# Schema for POST /usuarios (in case of "happy path" or success)
# Defines the success contract for user creation (POST). 
# Ensures that the API returns the confirmation message and the generated ID, 
# essential data for the front-end to validate the action.

create_user_success_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"}
    },
    "required": ["message", "_id"]
}

# ====================================================================

# Schema for GET /usuarios/{_id} (in case of "happy path" or success)
# Validates the complete return structure of a specific user (GET). 
# Ensures that the interface receives correctly typed data (such as the 
# string restriction on administrator), avoiding unexpected layout breaks.

get_user_schema = {
    "type": "object",
    "properties": {
        "nome": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
        "administrador": {
            "type": "string", 
            "enum": ["true", "false"] # Guarantee that the code will only accept these two strings
        },
        "_id": {"type": "string"}
    },
    "required": ["nome", "email", "password", "administrador", "_id"]
}

# ====================================================================

# Schema for GET /usuarios/{_id} (in case of "happy path" or success)
# Validates the complete return structure of a specific user (GET). 
# Ensures that the interface receives correctly typed data (such as the 
# string restriction on administrator), avoiding unexpected layout breaks.

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

# Schema for Login Error (401/404) and missing fields (400)
# Standardizes the exception contract for authentication failures (401/404).
# Ensures that the API returns the correct message key, allowing the 
# secure display of visual access denied feedback in the UI.

login_error_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
}

# ====================================================================

# Schemas for validation of missing fields in Registration (Error 400)
# Verifies the error contract (400) when the "nome" field is omitted in the 
# registration. Ensures that the response maps the failure exactly to the 
# corresponding key, ideal for signaling the error directly on the input.

missing_name_schema = {
    "type": "object",
    "properties": {"nome": {"type": "string"}},
    "required": ["nome"]
}

# ====================================================================

# Validates the response structure (400) for the absence of email in the 
# registration. Ensures that the error returns in the "email" key, facilitating 
# exception handling and clarity in the user interface.

missing_email_schema = {
    "type": "object",
    "properties": {"email": {"type": "string"}},
    "required": ["email"]
}

# ====================================================================

# Confirms the exception contract focused on the missing password field (400).
# Ensures that the API points out the error in the correct key, which is 
# fundamental for the user experience when trying to complete registration forms.

missing_password_schema = {
    "type": "object",
    "properties": {"password": {"type": "string"}},
    "required": ["password"]
}

# ====================================================================

# Defines the error structure for the omission of the administrator flag (400). 
# Ensures that the request precisely informs the missing field, maintaining 
# the consistency of the UI contracts.

missing_administrator_schema = {
    "type": "object",
    "properties": {"administrador": {"type": "string"}},
    "required": ["administrador"]
}

# ====================================================================

# Schema for POST /usuarios (in case of "happy path" or success)
# Defines the success contract for user creation (POST). 
# Ensures that the API returns the confirmation message and the generated ID, 
# essential data for the front-end to validate the action.

create_user_success_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"}
    },
    "required": ["message", "_id"]
}

# ====================================================================

# Schema for POST /usuarios
# Defines the error contract for user creation (POST) with a duplicated 
# email. Ensures that the API returns the error message.

duplicated_email_schema = { 
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
} 

# ====================================================================

# Schema for GET /usuarios (List all)
# Ensures that the API returns the amount of users and a list with 
# the complete data of each one, validating the display contract.

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

# Schema for PUT /usuarios
# Validates the success response (200) after updating a user,
# ensuring that the confirmation message is correctly received.

update_user_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
}

# ====================================================================

# Schema for PUT /usuarios (duplicated email)
# Validates the error response (400) when trying to update a user with
# an email that already exists in the system.

duplicated_email_update_user_schema = { 
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
} 

# ====================================================================

# Schema for POST /produtos
# Validates the success response (201) after creating a product,
# ensuring that the confirmation message and the generated ID are correctly 
# received.

create_product_success_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"}
    },
    "required": ["message", "_id"]
}

# ====================================================================

# Schema for POST /produtos (missing name)
# Validates the error response (400) when trying to create a product without 
# providing the "nome" field, ensuring that the server validation is triggered.

missing_product_name_schema = {
    "type": "object",
    "properties": {
        "nome": {"type": "string"}
    },
    "required": ["nome"]
}

# ====================================================================

# Schema for POST /produtos (missing price)
# Validates the error response (400) when trying to create a product without 
# providing the "preco" field, ensuring that the server validation is triggered.

missing_product_price_schema = { 
    "type": "object",
    "properties": {
        "preco": {"type": "string"}
    },
    "required": ["preco"]
}

# ====================================================================

# Schema for POST /produtos (missing description)
# Validates the error response (400) when trying to create a product without 
# providing the "descricao" field, ensuring that the server validation is triggered.

missing_product_description_schema = {
    "type": "object",
    "properties": {
        "descricao": {"type": "string"}
    },
    "required": ["descricao"]
}

# ====================================================================

# Schema for GET /produtos
# Validates the success response (200) after listing products,
# ensuring that the quantity and the product list are correctly 
# received.

list_all_products_schema = {
    "type": "object",
    "properties": {
        "quantidade": {"type": "integer"},
        "produtos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "preco": {"type": "number"},
                    "descricao": {"type": "string"},
                    "quantidade": {"type": "number"},
                    "_id": {"type": "string"}
                },
                "required": ["nome", "preco", "descricao", "quantidade", "_id"]
            }
        }
    },
    "required": ["message", "_id"]
}

# ====================================================================

# Schema for POST /carrinhos
# Validates the success response (201) after creating a cart,
# ensuring that the confirmation message and the generated ID are correctly 
# received.

create_cart_successfully_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"}
    },
    "required": ["message", "_id"]
}

# ====================================================================