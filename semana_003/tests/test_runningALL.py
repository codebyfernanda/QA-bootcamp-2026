# ======================================== ARQUIVO CRIADO POR FERNANDA BASTOS (@codebyfernanda) ========================================

from _pytest import hookspec
import subprocess
import sys
from pathlib import Path

# Define os caminhos das pastas
PASTA_TESTS = Path(__file__).parent
PASTA_RAIZ = PASTA_TESTS.parent

# Atualiza dependências automaticamente
subprocess.run(
    [sys.executable, "-m", "pip", "install", "--upgrade", "-r", str(PASTA_RAIZ / "requirements.txt")],
    check=True,
)

# Lista de arquivos de teste
testes = [
    # Teste inicial
    "test_if_API_is_online.py",

    # Testes de criação de usuário
    "test_create_user_successfully.py", 
    "test_create_user_duplicated_email.py",

    # Testes de busca de usuário
    "test_search_user_by_id.py",
    "test_search_user_by_nonexistent_id.py",

    # Teste de atualização de usuário
    "test_update_user_successfully.py", 
    "test_update_user_nonexistent_id.py",

    # Teste de exclusão de usuário
    "test_delete_user_successfully.py",

    # Teste de listagem de produto
    "test_list_all_products.py",

    # Teste de busca de produto
    "test_search_product_by_id.py",

    # Teste de atualização de produto
    "test_update_product.py",

    # Teste de exclusão de produto
    "test_delete_product.py",
]

if __name__ == "__main__":
    # Constrói o caminho completo para cada arquivo de teste
    arquivos = [str(PASTA_TESTS / t) for t in testes]
    
    # Executa os testes usando o pytest
    resultado = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"] + arquivos,
        cwd=str(PASTA_RAIZ),
    )
    
    # Sai com o código de retorno do pytest
    sys.exit(resultado.returncode)