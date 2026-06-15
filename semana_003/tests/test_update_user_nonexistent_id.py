# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest
import uuid

# Atualização de ID inexistente (201)
def test_update_user_nonexistent_id():
    user_id = "abc123xyz4567890" 
    url = f"https://compassuol.serverest.dev/usuarios/{user_id}"
    
    payload = {
        "nome": "Fernanda Bastos Atualizado",
        "email": f"teste_atualizado_{uuid.uuid4()}@qa.com.br",
        "password": "Teste!123",
        "administrador": "true"
    }
    
    try:
        response = requests.put(url, json=payload)
        response_body = response.json()
        
        print(f"\nCorpo da resposta da API (PUT em ID inexistente): {response_body}")
        
        # Como o ID não existe, o ServeRest cria um novo usuário
        assert response.status_code == 201
        
        assert "message" in response_body, f"A chave 'message' não veio na resposta! {response_body}"
        assert response_body["message"] == "Cadastro realizado com sucesso"
        
    except requests.exceptions.RequestException as error_update_user_nonexistent_id:
        pytest.fail(f"A requisição falhou devido a um erro de conexão: {error_update_user_nonexistent_id}")
