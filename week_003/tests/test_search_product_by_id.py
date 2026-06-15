# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

# Search Product by ID (GET)
def test_search_product_by_id(my_product_fixture):
    prod_id = my_product_fixture["id"]
    url = f"https://compassuol.serverest.dev/produtos/{prod_id}"

    try:
        response = requests.get(url)
        response_body = response.json()
        
        print(f"\nAPI response body (GET on existing ID): {response_body}")
        
        assert response.status_code == 200
        assert "_id" in response_body
        assert response_body["_id"] == prod_id
        print(f"\nStatus returned for SUCCESSFUL PRODUCT SEARCH BY ID: {response.status_code}")
        
    except requests.exceptions.RequestException as error_search_product_sucessfully:
        pytest.fail(f"The API is returning an error upon successful search. Error: {error_search_product_sucessfully}")

# ===================================================================================================================================
