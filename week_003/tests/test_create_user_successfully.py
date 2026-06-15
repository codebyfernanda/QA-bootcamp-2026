# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest
import uuid 

# Create registration successfully (201/200)
#   The data that will be sent (Use Payload)

def test_create_user_successfully():
    url = "https://compassuol.serverest.dev/usuarios"
    
    payload = { 
        "nome": "Fernanda Bastos",
        "email": f"fernandabastos_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }
    
    try:
        response = requests.post(url, json=payload)
        assert response.status_code in [200, 201]
        print(f"\nStatus returned for SUCCESSFUL REGISTRATION: {response.status_code}")
        
    except requests.exceptions.RequestException as error_create_user_successfully:
        pytest.fail(f"The API is returning an error. Error: {error_create_user_successfully}")

# ===================================================================================================================================
