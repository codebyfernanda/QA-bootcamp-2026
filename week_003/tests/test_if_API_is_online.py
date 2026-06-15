# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

ENDPOINT = "https://compassuol.serverest.dev/" 

# Testar se a API está online
def test_if_API_is_online():
    url = "https://compassuol.serverest.dev/"
    
    try:
        response = requests.get(url)
        assert response.status_code == 200
        print(f"\nStatus retornado para API ONLINE: {response.status_code}")
        
    except requests.exceptions.RequestException as error_not_online:
        pytest.fail(f"A API está offline ou inacessível. Erro: {error_not_online}")
