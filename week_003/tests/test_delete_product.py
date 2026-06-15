# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

# DELETE product 
def test_delete_product(my_product_fixture):
    prod_id = my_product_fixture["id"]
    token = my_product_fixture["token"]
    url = f"https://compassuol.serverest.dev/produtos/{prod_id}"
    
    headers = {
        "Authorization": token
    }

    try:
        response = requests.delete(url, headers=headers)
        response_body = response.json()
        
        print(f"\nAPI response body (DELETE on existing ID): {response_body}")
        
        assert response.status_code == 200
        
        assert "message" in response_body, f"The 'message' key was not found in the response! {response_body}"
        assert response_body["message"] == "Record deleted successfully"
        print(f"\nStatus returned for SUCCESSFUL PRODUCT DELETION: {response.status_code}")
        
    except requests.exceptions.RequestException as error_delete_product_sucessfully:
        pytest.fail(f"The API is returning an error upon product deletion. Error: {error_delete_product_sucessfully}")

# ===================================================================================================================================

