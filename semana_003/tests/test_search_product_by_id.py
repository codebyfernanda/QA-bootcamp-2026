# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

# Buscar Produto por ID (GET)
def test_search_product_by_id(my_product_fixture):
    prod_id = my_product_fixture["id"]
    url = f"https://compassuol.serverest.dev/produtos/{prod_id}"

    try:
        response = requests.get(url)
        response_body = response.json()
        
        print(f"\nCorpo da resposta da API (GET em ID existente): {response_body}")
        
        assert response.status_code == 200
        assert "_id" in response_body
        assert response_body["_id"] == prod_id
        print(f"\nStatus retornado para BUSCA DE PRODUTO POR ID COM SUCESSO: {response.status_code}")
        
    except requests.exceptions.RequestException as error_search_product_sucessfully:
        pytest.fail(f"A API está retornando um erro na busca com sucesso. Erro: {error_search_product_sucessfully}")
