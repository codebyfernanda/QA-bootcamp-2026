# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

import requests
import pytest

ENDPOINT = "https://compassuol.serverest.dev/" 

# Testing if API is online
def test_if_API_is_online():
    url = "https://compassuol.serverest.dev/"
    
    try:
        response = requests.get(url)
        assert response.status_code == 200
        print(f"\nStatus returned for ONLINE API: {response.status_code}")
        
    except requests.exceptions.RequestException as error_not_online:
        pytest.fail(f"The API is offline or unreachable. Error: {error_not_online}")

# ===================================================================================================================================
