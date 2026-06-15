# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

import requests 

# Falha ao cadastrar por causa de e-mail duplicado (400)
ENDPOINT= "https://compassuol.serverest.dev/usuarios" 


# O teste em si
def test_create_user_duplicated_email(my_user_fixture):
    payload = my_user_fixture["payload"]
    
    response = requests.post(ENDPOINT, json=payload)
    
    assert response.status_code == 400
    assert response.json()["message"] == "Este email já está sendo usado"
    print(f"\nStatus retornado para E-MAIL DUPLICADO: {response.status_code}.")
