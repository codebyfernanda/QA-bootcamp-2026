# Technical Challenge | AWS AI FDE Driven Quality Engineering Bootcamp 

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pytest-9.0-0A9EDC?logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/Coverage-100%25-brightgreen" />
  <img src="https://img.shields.io/badge/Status-Finished-success" />
</p>

This project consists of an automated test suite developed in **Python** using the **Pytest** framework. The primary objective is to validate the business rules and contracts of the *Users*, *Products*, *Login* and *Carts* endpoints of the public API [**ServeRest**](https://compassuol.serverest.dev/?lang=pt-BR#/), ensuring data integrity, system resilience and response accuracy.

---

## Architectural Evolution and Refactoring (Week 04)

During the [fourth week](https://github.com/codebyfernanda/bootcamp-QA-2026-desafios/tree/main/semana_004) of the Bootcamp, the project architecture was refactored following Quality Engineering best practices:

* **Domain-Driven Modularization:** Reorganized test files into clear modules based on context (Login, Users, Products and Carts), moving away from monolithic structures.
* **Adoption of the AAA Pattern (Arrange, Act, Assert):** Removed redundant `try/except` blocks that cluttered the code. The structure now strictly follows the *Arrange, Act, and Assert* flow, making tests focused and readable.
* **Base URL Centralization:** Created dedicated fixtures to manage the API base URL, eliminating string repetition across tests and facilitating seamless transitions between different testing environments.
* **State Management (Setup/Teardown):** Implemented automated database cleanup routines (`teardown`), ensuring complete independence between test scenarios.
* **Contract Testing:** Evolved from simple `status_code` and isolated key validations to full structural validation of the response payload using the `jsonschema` library.

---

## Test Plan

<details>
<summary><b>1. Objective and Strategy</b></summary>

* **Objective:** Ensure functional quality, contract stability and reliability.
* **Strategy:** Automation of functional and contract tests at the API layer.
* **Tech Stack:** Python 3.13.x, Pytest, Requests and JSONSchema.
* **Scope:** `/login`, `/usuarios`, `/produtos` and `/carrinhos` endpoints.
* **Out of Scope:** Load, stress and performance testing.
</details>

<details>
<summary><b>2. Mapped Test Scenarios</b></summary>

* **`test_login.py`**: Authentication suite (success and failure scenarios).
* **`test_usuarios.py`**: Full CRUD operations with email validation.
* **`test_produtos.py`**: Product management and admin token validation.
* **`test_carrinhos.py`**: Purchase management, stock constraints and order cancellation.
</details>

<details>
<summary><b>3. Definition of Done (DoD)</b></summary>

- [x] Naming convention: `test_<action>_<expected_result>`.
- [x] Centralized *fixtures* (`conftest.py`).
- [x] Dynamic test data (UUID).
- [x] Full structural validation via `JSON Schema`.
</details>

## Project Structure
```
QA-bootcamp-2026/
│
├── .github/
│   └── workflows/
│       └── ci.yml               # CI/CD configuration (GitHub Actions)
│
├── semana_003/                  # Sprint 3 Challenges
│   ├── tests/
│   │   ├── test_create_user_duplicated_email.py
│   │   ├── test_create_user_successfully.py
│   │   ├── test_delete_product.py
│   │   ├── test_delete_user_successfully.py
│   │   ├── test_if_API_is_online.py
│   │   ├── test_list_all_products.py
│   │   ├── test_runningALL.py
│   │   ├── test_search_product_by_id.py
│   │   ├── test_search_user_by_id.py
│   │   ├── test_search_user_by_nonexistent_id.py
│   │   ├── test_update_product.py
│   │   ├── test_update_user_nonexistent_id.py
│   │   └── test_update_user_successfully.py
│   └── conftest.py              # Fixtures for Sprint 3
│   └── requirements.txt         # Python project dependencies
│
├── semana_004/                  # Sprint 4 Challenges
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── schemas.py           # JSON Schemas for validation
│   │   ├── test_carrinhos.py
│   │   ├── test_login.py
│   │   ├── test_produtos.py
│   │   └── test_usuarios.py
│   └── conftest.py              # Fixtures for Sprint 4
│   └── requirements.txt         # Python project dependencies
|
├── README.md                    # Project documentation
└── Dockerfile                   # Docker configuration for isolated test execution environment
└── package.json                 # Node dependencies for auxiliary tools
└── requirements.txt             # Python project dependencies
```

## Metrics & Results

### Test Coverage
To ensure the robustness and quality of the API, the automation strategy was based on the **Operator Coverage** methodology. This approach measures the extent of tested HTTP methods in relation to the available endpoints.

### Operations Coverage Map

| Endpoint | POST | GET | PUT | DELETE | Total Operations |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `/login` | ✅ | - | - | - | 1 |
| `/usuarios` | ✅ | ✅ | ✅ | ✅ | 4 |
| `/produtos` | ✅ | ✅ | ✅ | ✅ | 4 |
| `/carrinhos` | - | - | ✅ | ✅ | 2 |
| **Totals** | **4** | **2** | **3** | **2** | **11 / 11** |

### Calculation Methodology

The calculation was performed using the **Operator Coverage** formula:

Since the API exposes 11 distinct operations across the four resources (Login, Users, Products and Carts) and all flows have been properly automated, the test suite has achieved **100% operation coverage**.

### Quality Beyond Coverage

Beyond achieving 100% operator coverage, the suite focuses on the quality of validations:

* **Status Code Coverage:** Validation of successful flows (200, 201) and expected error scenarios (400, 401, 403, 404).
* **JSON Schema Validation:** Guarantee that the API contract is respected in every response, ensuring the Front-End receives the expected data format.
* **Integration Flows:** Tests that orchestrate dependencies, such as creating a product for subsequent use in cart creation, simulating real-world system usage.

--- 

### Bugs and Inconsistencies Found

| Severity | Bug / Inconsistency | Expected Behavior | Actual Behavior |
| :--- | :--- | :--- | :--- |
| 🔴 **Critical** | **Privilege Escalation** | The system must prevent a standard user from changing their profile to `administrador: true`. | The `PUT /usuarios/{id}` endpoint allows the change, promoting the user to administrator. |
| 🔵 **Low** | **Response Inconsistency (Empty Payload)** | Return a standardized validation error (`400`) on all routes when receiving `{}`. | Returns `400` on public routes and `401` on private routes for the same payload. |

---

## Main Challenges and Lessons Learned

| Challenge | Solution |
| :--- | :--- |
| **Contract Validation (JSON Schema)** | Mapped specific error keys per field (e.g., `"nome": "nome é obrigatório"`) instead of generic keys, facilitating error handling on the Front-End. |
| **HTTP Verb Response** | Strategic separation between mutation schemas (only `message` and `_id`) and reading schemas (full object), adjusting validation expectations. |
| **Request Chaining** | Implementation of chained flows (POST Product > Extract `_id` > Build Payload > POST Cart) to respect the API's relational architecture. |
| **Data Mutability** | Used the `.copy()` method on dictionaries to prevent data manipulation in one test from affecting the original fixture state in subsequent tests. |
| **Pytest Rigor (Naming)** | Developed a critical reading approach to Pytest error logs to quickly identify naming mismatches between fixtures and injected parameters. |
| **Development Environment** | Increased attention to visual file-saving indicators in VS Code, eliminating false positives caused by running outdated code. |

---

## Conclusion

This challenge was a deep dive into what it truly means to be a Quality Engineer in practice. As our instructor Jacques Schmitz mentioned in our 1st Workshop, **"QA acts throughout the entire cycle, acting as a facilitator for the team—influencing design, assisting with observability and managing how to handle the volume of data generated by the business."** I realized that when we structure well-organized tests, our mission is not just to find bugs, but to prevent problems from arising while simultaneously reducing business risks.

Far beyond simply automating manual tasks, we are building a safety layer "to have peace of mind and security regarding changes" and to "ensure that changes do not break other aspects of the code," as stated by Professor José Correia, Software Quality Specialist, in the *Início Rápido em Teste e QA* course available on Udemy (which we studied during the first week of the Bootcamp).

The refactoring I carried out during this fourth week gave me a valuable insight: **quality is an intrinsic part of architecture, and as QAs, we must act throughout the entire application lifecycle** (as indicated by the shift-left approach), a topic covered in our second-week quiz. When we treat API contracts with the same care that we treat the user interface, we help everyone realize "that quality is a team effort and vital for the product," a concept emphasized by Correia.

In this way, we ensure that the entire ecosystem speaks the same language. **Reflecting on this entire experience: I feel even more motivated and equipped with a stronger toolkit to apply this strategic vision in business scenarios, acting as an active project member who provides guidance on quality.**

---

## References

* [AAA Pattern in Test Automation - Semaphore CI](https://semaphore.io/blog/aaa-pattern-test-automation)
* [Pytest Documentation & Best Practices](https://docs.pytest.org/)
* [Pytest: Help your tests do more](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
* [How to verify REST API test coverage](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b)
* [Test Coverage Criteria for RESTful Web APIs](https://www.researchgate.net/publication/327774902_Test_coverage_criteria_for_RESTful_web_APIs) 
* [Introduction to Contract Testing](https://martinfowler.com/articles/contract-testing.html)
* [Understanding JSON Schema](https://json-schema.org/learn/getting-started-step-by-step) 

---

### How to Run This Repository

1. **Clone the repository:**
```bash
git clone <https://github.com/codebyfernanda/QA-bootcamp-2026.git>
cd QA-bootcamp-2026

```

2. **Create and activate a virtual environment:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

```

```
# Linux/macOS
python -m venv venv
source venv/bin/activate

```

3. **Install the dependencies:**

```bash
pip install -r requirements.txt

```

4. **Run the tests:**

```bash
pytest -v

```
---

## About the Author & Acknowledgments

This project was developed by **Fernanda Bastos dos Santos** [(@codebyfernanda)](https://github.com/codebyfernanda), a student of **Analysis and Systems Development** at Mackenzie, during the **BOOTCAMP | AWS AI FDE DRIVEN QUALITY ENGINEERING** hosted by Compass UOL in partnership with [AI/R Company](https://aircompany.ai/).

I would like to express my sincere gratitude to Squad 2 for their engagement, knowledge sharing and support throughout our bootcamp journey. A special thanks goes to my colleagues [Renan Pacheco](https://github.com/Renanpacheco) and [Vitor Kunicki](https://github.com/vitto2099) — your patience, availability and guidance were fundamental in helping me overcome the challenges of this delivery. 

I would also like to take this opportunity to thank my instructors, Amanda Almeida and [Jacques Schmitz](https://github.com/juniorschmitz), for their continuous support and readiness to help with technical content during our training, as well as our Scrum Master, Leticia Souza, for her daily guidance and sensitivity toward our journey in the program. Thank you so much! :)
 
