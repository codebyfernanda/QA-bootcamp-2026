# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest
import uuid

# Atualização de usuário com sucesso (200)
def test_update_user_successfully(my_user_fixture):
    user_id = my_user_fixture["id"]
    url = f"https://compassuol.serverest.dev/usuarios/{user_id}"
    
    payload = {
        "nome": "Fernanda Bastos Atualizado",
        "email": f"teste_atualizado_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }
    
    try:
        response = requests.put(url, json=payload)
        assert response.status_code == 200
        assert response.json()["message"] == "Registro alterado com sucesso"
        print(f"\nStatus retornado para ATUALIZAÇÃO DE USUÁRIO COM SUCESSO: {response.status_code}")
        
    except requests.exceptions.RequestException as error_update_user:
        pytest.fail(f"A API retornou um erro na atualização do usuário. Erro: {error_update_user}")