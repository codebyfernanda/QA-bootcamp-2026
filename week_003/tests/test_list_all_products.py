import requests
import pytest

# Listar todos os produtos
def test_list_all_products():
    url = "https://compassuol.serverest.dev/produtos"
    
    try:
        response = requests.get(url)
        assert response.status_code == 200
        assert "produtos" in response.json()
        print(f"\nStatus retornado para LISTAR TODOS OS PRODUTOS: {response.status_code}")
        
    except requests.exceptions.RequestException as error_list_all_products:
        pytest.fail(f"A API está retornando um erro na listagem de todos os produtos. Erro: {error_list_all_products}")
