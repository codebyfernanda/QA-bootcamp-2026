# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest
import uuid 

# Atualizar Produto (PUT)
def test_update_product(my_product_fixture):
    prod_id = my_product_fixture["id"]
    token = my_product_fixture["token"]
    url = f"https://compassuol.serverest.dev/produtos/{prod_id}"
    
    payload = {
        "nome": f"Logitech MX Vertical ATUALIZADO {uuid.uuid4()}",
        "preco": 500,
        "descricao": "Mouse ergonômico",
        "quantidade": 100
    }
    
    headers = {
        "Authorization": token
    }
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        response_body = response.json()
        
        print(f"\nCorpo da resposta da API (PUT em ID existente): {response_body}")
        
        assert response.status_code == 200
        
        assert "message" in response_body, f"A chave 'message' não veio na resposta! {response_body}"
        assert response_body["message"] == "Registro alterado com sucesso"
        print(f"\nStatus retornado para ATUALIZAÇÃO DE PRODUTO COM SUCESSO: {response.status_code}")
        
    except requests.exceptions.RequestException as error_update_product_sucessfully:
        pytest.fail(f"A API está retornando um erro na atualização do produto. Erro: {error_update_product_sucessfully}")
