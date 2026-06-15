# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

# Deleted successfully (200)
def test_delete_user_successfully(my_user_fixture):   
    user_id = my_user_fixture["id"]
    url = f"https://compassuol.serverest.dev/usuarios/{user_id}"
    
    try:
        response = requests.delete(url)
        response_body = response.json()
        
        print(f"\nAPI response body (DELETE by existing ID): {response_body}")
        
        assert response.status_code == 200
        
        assert "message" in response_body,f"The 'message' key is missing from the response! {response_body}"
        assert response_body["message"] == "Record deleted successfully"
        print(f"\nStatus returned for SUCCESSFUL DELETE: {response.status_code}")
        
    except requests.exceptions.RequestException as error_delete_user_sucessfully:
        pytest.fail(f"The API is throwing an error on successful deletion. Error: {error_delete_user_sucessfully}") 
