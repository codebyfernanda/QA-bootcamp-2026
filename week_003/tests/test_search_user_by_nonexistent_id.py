# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

# Search by non-existent ID (400)
def test_search_user_by_nonexistent_id():
# Valid ID that does not exist in the database (exactly 16 alphanumeric characters)    
    nonexistent_id = "abc123xyz4567890" 
    url = f"https://compassuol.serverest.dev/usuarios/{nonexistent_id}"
    
    try:
        response = requests.get(url)
        response_body = response.json()
        
        print(f"\nAPI response body: {response_body}")
        
        assert response.status_code == 400
        assert "message" in response_body, f"The 'message' key was not found in the response! API Response: {response_body}"
        assert response_body["message"] == "User not found"
        
    except requests.exceptions.RequestException as error_search_nonexistent_id:
        pytest.fail(f"The request failed due to a connection error: {error_search_nonexistent_id}") 

# ===================================================================================================================================
