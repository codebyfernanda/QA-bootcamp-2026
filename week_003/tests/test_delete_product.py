# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

# Excluir Produto (DELETE)
def test_delete_product(my_product_fixture):
    prod_id = my_product_fixture["id"]
    token = my_product_fixture["token"]
    url = f"https://compassuol.serverest.dev/produtos/{prod_id}"
    
    headers = {
        "Authorization": token
    }

    try:
        response = requests.delete(url, headers=headers)
        response_body = response.json()
        
        print(f"\nCorpo da resposta da API (DELETE em ID existente): {response_body}")
        
        assert response.status_code == 200
        
        assert "message" in response_body, f"A chave 'message' não veio na resposta! {response_body}"
        assert response_body["message"] == "Registro excluído com sucesso"
        print(f"\nStatus retornado para EXCLUSÃO DE PRODUTO COM SUCESSO: {response.status_code}")
        
    except requests.exceptions.RequestException as error_delete_product_sucessfully:
        pytest.fail(f"A API está retornando um erro na exclusão do produto. Erro: {error_delete_product_sucessfully}")
