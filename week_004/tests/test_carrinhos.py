# ======= ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) =======

# test_carrinhos.py
# Módulo responsável por executar os testes de Carrinhos e CRUD
# Contendo 4 testes
import requests
from jsonschema import validate
from tests.schemas import (
    create_cart_successfully_schema,
)

# test_create_cart_successfully (POST - 201)
# Valida a criação de um carrinho com produto, garantindo que o POST 
# retorne 201 e que o contrato seja respeitado.
  
def test_create_cart_successfully(carts_url, products_url, admin_auth_headers, valid_product_payload):
    # 1. Cria o produto primeiro para ter um ID real
    prod_response = requests.post(products_url, json=valid_product_payload, headers=admin_auth_headers)
    product_id = prod_response.json()["_id"]
    
    # 2. Monta o payload do carrinho com o ID gerado
    cart_payload = {
        "produtos": [
            {
                "idProduto": product_id,
                "quantidade": 1
            }
        ]
    }

    # 3. Cria o carrinho
    create_response = requests.post(carts_url, json=cart_payload, headers=admin_auth_headers)

    # 4. Validações
    assert create_response.status_code == 201
    assert create_response.json()["message"] == "Cadastro realizado com sucesso"
    
    validate(instance=create_response.json(), schema=create_cart_successfully_schema)

    # 5. Teardown duplo (Cancelar para limpar o carrinho e deletar o produto)
    requests.delete(f"{carts_url}/cancelar-compra", headers=admin_auth_headers)
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================

# test_create_cart_insufficient_stock (POST - 400)
# Valida a criação de um carrinho com produto, garantindo que o POST 
# retorne 400 e que o contrato seja respeitado.

def test_create_cart_insufficient_stock(carts_url, products_url, admin_auth_headers, valid_product_payload, payload_factory):
    # 1. Cria o produto
    prod_response = requests.post(products_url, json=valid_product_payload, headers=admin_auth_headers)
    product_id = prod_response.json()["_id"]
    
    # 2. Usa a factory para criar o payload com o ID correto
    payload = payload_factory(product_id, 50)

    # 3. Faz a requisição
    create_response = requests.post(carts_url, json=payload, headers=admin_auth_headers)

    # 4. Validações
    assert create_response.status_code == 400
    assert create_response.json()["message"] == "Produto não possui quantidade suficiente"

    # 5. Teardown
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================

# test_conclude_purchase_successfully (DELETE - 200)
# Valida a conclusão de uma compra, garantindo que o DELETE 
# retorne 200 e que o contrato seja respeitado.

def test_conclude_purchase_successfully(carts_url, products_url, admin_auth_headers, valid_product_payload):
    # 1. Preparação: Cria produto e cria o carrinho
    prod_response = requests.post(products_url, json=valid_product_payload, headers=admin_auth_headers)
    product_id = prod_response.json()["_id"]
    
    cart_payload = {"produtos": [{"idProduto": product_id, "quantidade": 1}]}
    requests.post(carts_url, json=cart_payload, headers=admin_auth_headers)

    # 2. Ação: Concluir a compra
    delete_response = requests.delete(f"{carts_url}/concluir-compra", headers=admin_auth_headers)

    # 3. Validações
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Registro excluído com sucesso"

    # Teardown (só o produto, pois concluir a compra já destrói o carrinho)
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)
    
# ====================================================================

# test_cancel_purchase_and_stock_return (DELETE - 200)
# Valida o cancelamento de uma compra, garantindo que o DELETE 
# retorne 200 e que o contrato seja respeitado.

def test_cancel_purchase_and_stock_return(carts_url, products_url, admin_auth_headers, valid_product_payload):
    # 1. Preparação: Cria produto e cria o carrinho
    prod_response = requests.post(products_url, json=valid_product_payload, headers=admin_auth_headers)
    product_id = prod_response.json()["_id"]
    
    cart_payload = {"produtos": [{"idProduto": product_id, "quantidade": 1}]}
    requests.post(carts_url, json=cart_payload, headers=admin_auth_headers)

    # 2. Ação: Cancelar a compra
    delete_response = requests.delete(f"{carts_url}/cancelar-compra", headers=admin_auth_headers)

    # 3. Validações
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Registro excluído com sucesso. Estoque dos produtos reabastecido"

    # Teardown (só o produto, pois cancelar a compra já destrói o carrinho)
    requests.delete(f"{products_url}/{product_id}", headers=admin_auth_headers)

# ====================================================================
