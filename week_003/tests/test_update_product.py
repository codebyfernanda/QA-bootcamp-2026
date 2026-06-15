# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest
import uuid 

# Update Product (PUT)
def test_update_product(my_product_fixture):
    prod_id = my_product_fixture["id"]
    token = my_product_fixture["token"]
    url = f"https://compassuol.serverest.dev/produtos/{prod_id}"
    
    payload = {
        "nome": f"Logitech MX UPDATED {uuid.uuid4()}",
        "preco": 500,
        "descricao": "Mouse",
        "quantidade": 100
    }
    
    headers = {
        "Authorization": token
    }
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        response_body = response.json()
        
        print(f"\nAPI response body (PUT on existing ID): {response_body}")
        
        assert response.status_code == 200
        
        assert "message" in response_body, f"The 'message' key was not found in the response! {response_body}"
        assert response_body["message"] == "Record updated successfully"
        print(f"\nStatus returned for SUCCESSFUL PRODUCT UPDATE: {response.status_code}")
        
    except requests.exceptions.RequestException as error_update_product_sucessfully:
        pytest.fail(f"The API is returning an error upon product update. Error: {error_update_product_sucessfully}")

# ===================================================================================================================================
