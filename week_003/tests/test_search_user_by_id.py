# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

# Search by existing ID
def test_search_user_by_id(my_user_fixture):
    user_id = my_user_fixture["id"]
    url = f"https://compassuol.serverest.dev/usuarios/{user_id}"
    
    try:
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json()["_id"] == user_id
        print(f"\nStatus returned for SEARCH BY EXISTING ID: {response.status_code}")
        
    except requests.exceptions.RequestException as error_search_user_existent:
        pytest.fail(f"The API is returning an error when searching by an existing ID. Error: {error_search_user_existent}")

# ===================================================================================================================================
