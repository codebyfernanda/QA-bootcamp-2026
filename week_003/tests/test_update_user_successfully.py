# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest
import uuid

# Successful user update (200)
def test_update_user_successfully(my_user_fixture):
    user_id = my_user_fixture["id"]
    url = f"https://compassuol.serverest.dev/usuarios/{user_id}"
    
    payload = {
        "nome": "Fernanda Bastos Updated",
        "email": f"updatetesting{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }
    
    try:
        response = requests.put(url, json=payload)
        assert response.status_code == 200
        assert response.json()["message"] == "Registro alterado com sucesso"
        print(f"\nStatus returned for SUCCESSFUL USER UPDATE: {response.status_code}")
        
    except requests.exceptions.RequestException as error_update_user:
        pytest.fail(f"The API returned an error upon user update. Error: {error_update_user}")

# ===================================================================================================================================
