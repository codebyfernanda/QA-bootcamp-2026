# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

# Buscar por ID existente
def test_search_user_by_id(my_user_fixture):
    user_id = my_user_fixture["id"]
    url = f"https://compassuol.serverest.dev/usuarios/{user_id}"
    
    try:
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json()["_id"] == user_id
        print(f"\nStatus retornado para BUSCA POR ID EXISTENTE: {response.status_code}")
        
    except requests.exceptions.RequestException as error_search_user_existent:
        pytest.fail(f"A API está retornando um erro na busca por ID existente. Erro: {error_search_user_existent}")
