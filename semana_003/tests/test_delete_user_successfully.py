# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

# Exclusão com sucesso (200)
def test_delete_user_successfully(my_user_fixture):   
    user_id = my_user_fixture["id"]
    url = f"https://compassuol.serverest.dev/usuarios/{user_id}"
    
    try:
        response = requests.delete(url)
        response_body = response.json()
        
        print(f"\nCorpo da resposta da API (DELETE em ID existente): {response_body}")
        
        assert response.status_code == 200
        
        assert "message" in response_body, f"A chave 'message' não veio na resposta! {response_body}"
        assert response_body["message"] == "Registro excluído com sucesso"
        print(f"\nStatus retornado para EXCLUSÃO COM SUCESSO: {response.status_code}")
        
    except requests.exceptions.RequestException as error_delete_user_sucessfully:
        pytest.fail(f"A API está retornando um erro na exclusão com sucesso. Erro: {error_delete_user_sucessfully}") 
