# ======================================== FILE CREATED BY FERNANDA BASTOS (@codebyfernanda) ========================================

from _pytest import hookspec
import subprocess
import sys
from pathlib import Path

# Defines folder paths
PASTA_TESTS = Path(__file__).parent
PASTA_RAIZ = PASTA_TESTS.parent

# Automatically updates dependencies
subprocess.run(
    [sys.executable, "-m", "pip", "install", "--upgrade", "-r", str(PASTA_RAIZ / "requirements.txt")],
    check=True,
)

# List of test files
testes = [
    # Initial testing
    "test_if_API_is_online.py",

    # User creation tests
    "test_create_user_successfully.py", 
    "test_create_user_duplicated_email.py",

    # User search tests
    "test_search_user_by_id.py",
    "test_search_user_by_nonexistent_id.py",

    # # User update test
    "test_update_user_successfully.py", 
    "test_update_user_nonexistent_id.py",

    # User deletion test
    "test_delete_user_successfully.py",

    # Product listing test
    "test_list_all_products.py",

    # Product search test
    "test_search_product_by_id.py",

    # Product update test
    "test_update_product.py",

    # Product deletion test
    "test_delete_product.py",
]

if __name__ == "__main__":
    # Builds the full path for each test file
    arquivos = [str(PASTA_TESTS / t) for t in testes]
    
    # Runs the tests using pytest
    resultado = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"] + arquivos,
        cwd=str(PASTA_RAIZ),
    )
    
    # Exits with the pytest return code
    sys.exit(resultado.returncode)

# ===================================================================================================================================
