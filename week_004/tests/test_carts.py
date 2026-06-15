# ======= FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) =======

# test_carts.py
# Module responsible for executing Cart and CRUD tests
# 4 tests

import requests
from jsonschema import validate
from tests.schemas import (
    create_cart_successfully_schema,
)

# test_create_cart_successfully (POST - 201)
# Validates the creation of a cart with a product, ensuring that the POST 
# returns 201 and that the contract is respected.
  
def test_create_cart_successfully(carts_url, products_url, admin_auth_headers, valid_product_payload):
    # 1. Creates the product first to get a real ID
    prod_response = requests.post(products_url, json=valid_product_payload, headers=admin_auth_headers)
    product_id = prod_response.json()["_id"]
    
    # 2. Builds the cart payload with the generated ID
    cart_payload = {
        "produtos": [
            {
                "idProduto": product_id,
                "quantidade": 1
            }
        ]
    }

    # 3. Creates the cart
    create_response = requests.post(carts_url, json=cart_payload, headers=admin_auth_headers)

    # 4. Validations
    assert create_response.status_code == 201
    assert create_response.json()["message"] == "Cadastro realizado com sucesso"
    
    validate(instance=create_response.json(), schema=create_cart_successfully_schema)

    # 5. Double teardown (Cancel to clear the cart and delete the product)
    requests.delete(f"{carts_url}/cancelar-compra", headers=admin_auth_headers)
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================

# test_create_cart_insufficient_stock (POST - 400)
# Validates the creation of a cart with a product, ensuring that the POST 
# returns 400 and that the contract is respected.

def test_create_cart_insufficient_stock(carts_url, products_url, admin_auth_headers, valid_product_payload, payload_factory):
    # 1. Creates the product
    prod_response = requests.post(products_url, json=valid_product_payload, headers=admin_auth_headers)
    product_id = prod_response.json()["_id"]
    
    # 2. Uses the factory to create the payload with the correct ID
    payload = payload_factory(product_id, 50)

    # 3. Makes the request
    create_response = requests.post(carts_url, json=payload, headers=admin_auth_headers)

    # 4. Validations
    assert create_response.status_code == 400
    assert create_response.json()["message"] == "Produto não possui quantidade suficiente"

    # 5. Teardown
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================

# test_conclude_purchase_successfully (DELETE - 200)
# Validates the conclusion of a purchase, ensuring that the DELETE 
# returns 200 and that the contract is respected.

def test_conclude_purchase_successfully(carts_url, products_url, admin_auth_headers, valid_product_payload):
    # 1. Setup: Creates product and creates the cart
    prod_response = requests.post(products_url, json=valid_product_payload, headers=admin_auth_headers)
    product_id = prod_response.json()["_id"]
    
    cart_payload = {"produtos": [{"idProduto": product_id, "quantidade": 1}]}
    requests.post(carts_url, json=cart_payload, headers=admin_auth_headers)

    # 2. Action: Conclude purchase
    delete_response = requests.delete(f"{carts_url}/concluir-compra", headers=admin_auth_headers)

    # 3. Validations
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Registro excluído com sucesso"

    # Teardown (only the product, since concluding the purchase already destroys the cart)
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)
    
# ====================================================================

# test_cancel_purchase_and_stock_return (DELETE - 200)
# Validates the cancellation of a purchase, ensuring that the DELETE 
# returns 200 and that the contract is respected.

def test_cancel_purchase_and_stock_return(carts_url, products_url, admin_auth_headers, valid_product_payload):
    # 1. Setup: Creates product and creates the cart
    prod_response = requests.post(products_url, json=valid_product_payload, headers=admin_auth_headers)
    product_id = prod_response.json()["_id"]
    
    cart_payload = {"produtos": [{"idProduto": product_id, "quantidade": 1}]}
    requests.post(carts_url, json=cart_payload, headers=admin_auth_headers)

    # 2. Action: Cancel purchase
    delete_response = requests.delete(f"{carts_url}/cancelar-compra", headers=admin_auth_headers)

    # 3. Validations
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Registro excluído com sucesso. Estoque dos produtos reabastecido"

    # Teardown (only the product, since cancelling the purchase already destroys the cart)
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================