# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests 

ENDPOINT= "https://compassuol.serverest.dev/usuarios" 

# The test
def test_create_user_duplicated_email(my_user_fixture):
    payload = my_user_fixture["payload"]
    
    response = requests.post(ENDPOINT, json=payload)
    
    assert response.status_code == 400
    assert response.json()["message"] == "This email is already being used"
    print(f"\nStatus returned for DUPLICATE E-MAIL: {response.status_code}.")

# ===================================================================================================================================
