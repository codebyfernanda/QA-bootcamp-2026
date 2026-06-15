# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

# Busca por ID inexistente (400)
def test_search_user_by_nonexistent_id():
    # ID válido (formato correto) que não existe no banco (exatamente 16 caracteres alfanuméricos)
    nonexistent_id = "abc123xyz4567890" 
    url = f"https://compassuol.serverest.dev/usuarios/{nonexistent_id}"
    
    try:
        response = requests.get(url)
        response_body = response.json()
        
        print(f"\nCorpo da resposta da API: {response_body}")
        
        assert response.status_code == 400
        assert "message" in response_body, f"A chave 'message' não veio na resposta! Resposta da API: {response_body}"
        assert response_body["message"] == "Usuário não encontrado"
        
    except requests.exceptions.RequestException as error_search_nonexistent_id:
        pytest.fail(f"A requisição falhou devido a um erro de conexão: {error_search_nonexistent_id}") 
