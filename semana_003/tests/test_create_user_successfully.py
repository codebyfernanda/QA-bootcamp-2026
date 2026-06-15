# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest
import uuid 

# Criar cadastro com sucesso (201/200)
#   Os dados que serão enviados (Usar Payload)
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
        print(f"\nStatus retornado para CADASTRO COM SUCESSO: {response.status_code}")
        
    except requests.exceptions.RequestException as error_create_user_successfully:
        pytest.fail(f"A API está retornando um erro. Erro: {error_create_user_successfully}")