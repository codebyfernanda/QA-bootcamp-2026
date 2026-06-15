# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest
import uuid

# Update non-existent ID (201)
def test_update_user_nonexistent_id():
    user_id = "abc123xyz4567890" 
    url = f"https://compassuol.serverest.dev/usuarios/{user_id}"
    
    payload = {
        "nome": "Fernanda Bastos Updated",
        "email": f"testing{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }
    
    try:
        response = requests.put(url, json=payload)
        response_body = response.json()
        
        print(f"\nAPI response body (PUT on non-existent ID): {response_body}")
        
        # Since the ID does not exist, ServeRest creates a new user
        assert response.status_code == 201
        
        assert "message" in response_body, f"The 'message' key was not found in the response! {response_body}"
        assert response_body["message"] == "Cadastro realizado com sucesso"
        
    except requests.exceptions.RequestException as error_update_user_nonexistent_id:
        pytest.fail(f"The request failed due to a connection error: {error_update_user_nonexistent_id}")

# ===================================================================================================================================
