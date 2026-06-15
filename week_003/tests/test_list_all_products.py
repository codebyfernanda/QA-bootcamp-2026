# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

# Listar todos os produtos
def test_list_all_products():
    url = "https://compassuol.serverest.dev/produtos"
    
    try:
        response = requests.get(url)
        assert response.status_code == 200
        assert "produtos" in response.json()
        print(f"\nStatus returned for LIST ALL PRODUCTS: {response.status_code}")
        
    except requests.exceptions.RequestException as error_list_all_products:
        pytest.fail(f"The API is returning an error when listing all products. Error: {error_list_all_products}")

# ===================================================================================================================================
