# Test Plan — Test Suite Evolution (Serverest API)

This document establishes the automation strategy, execution scope, scenario mapping, and quality benchmarks designed for the integration test layer of the **ServeRest API**. It serves as the definitive engineering blueprint for the continuous evolution of our test suite.

---

## 1. Test Suite Objective
The primary objective of this suite is to secure the reliability, stability, contract integrity, and strict enforcement of business logic and Role-Based Access Control (RBAC) across the target endpoints. The architecture is engineered to validate resilient happy paths while aggressively catching malformed payloads, invalid operations, and critical security flaws such as privilege escalation.

## 2. Testing Strategy
Our strategy prioritizes speed, strict thread isolation, and deterministic test execution across both local environments and remote cloud infrastructure.

* **Test Layer:** API / Service / Integration Testing Layer.
* **Test Types:** Functional Validations (Positive & Negative flows) + Contract Compliance (JSON Schema verification).
* **Core Technology Stack:**
  * **Language:** Python 3.12
  * **Test Framework:** `pytest` (for orchestration, parametric testing, and fixture management).
  * **HTTP Client:** `requests` (for network transmission and payload consumption).
  * **Contract Validation:** `pytest-schema` (powered by `jsonschema` definitions).
  * **Infrastructure Isolation:** `Docker` (built atop `python:3.12-slim` for consistent, environment-agnostic execution).

## 3. Scope Matrix

### 🟢 In Scope
* **User Management (`/usuarios`):** Complete CRUD mutations, email uniqueness constraints, and input field integrity.
* **Authentication Lifecycle (`/login`):** Token generation mechanics, validation of credentials, and security boundary responses.
* **Product Catalog (`/produtos`):** Protected administrative inventory controls and role-based access restrictions.
* **Shopping Carts (`/carrinhos`):** Multi-dependency checkouts and automatic inventory restocking validation.

### 🔴 Out of Scope
* Performance benchmarks, load testing, or concurrency stress thresholds.
* Core infrastructure penetration testing or cryptographic token breaking.
* Front-End UI / End-to-End browser test automation.

---

## 4. Mapped & Implemented Test Scenarios

### Authentication Lifecycle (`/login` & `/usuarios`)
* **Scenario 01 (Positive) `test_create_user_successfully`:** Registers a baseline account via `POST /usuarios`, asserts a `201 Created` status with an integrated schema validation, and triggers an automated downstream `DELETE` teardown to guarantee a stateless database.
* **Scenario 02 (Negative) `test_login_invalid_password`:** Dispatches an authentication attempt via `POST /login` with an unverified password, asserting a strict `401 Unauthorized` block.
* **Scenario 03 (Negative) `test_login_nonexistent_user`:** Submits unregistered credentials to `/login`, verifying that the API gracefully rejects the transaction via standard `401`/`404` error envelopes to maintain user privacy.
* **Scenario 04 (Negative) `test_login_without_name`:** Rejects input creation on `/usuarios` when the `nome` key is dropped, expecting an explicit `400 Bad Request` and field-specific validation strings.
* **Scenario 05 (Negative) `test_login_without_email`:** Rejects input creation on `/usuarios` when the `email` key is dropped, expecting an explicit `400 Bad Request` and field-specific validation strings.
* **Scenario 06 (Negative) `test_login_without_password`:** Rejects input creation on `/usuarios` when the `password` key is dropped, expecting an explicit `400 Bad Request` and field-specific validation strings.
* **Scenario 07 (Negative) `test_login_without_administrator`:** Rejects input creation on `/usuarios` when the boolean `administrador` flag is omitted, returning a `400 Bad Request`.

### User Administration CRUD (`/usuarios`)
* **Scenario 01 (Positive) `test_create_user_successfully`:** Validates account provisioning via `POST`, verifying payload metadata and cascading cleanups.
* **Scenario 02 (Negative) `test_create_user_duplicated_email`:** Enforces backend data constraints by attempting a duplicate user registration, verifying that the engine catches conflicts and returns a `400 Bad Request` containing the specific error string.
* **Scenario 03 (Positive) `test_list_all_users`:** Targets a global `GET /usuarios`, confirming a `200 OK` status and validating that the structural multi-user array matches expectations.
* **Scenario 04 (Positive) `test_delete_user_successfully_by_id`:** Sequentially registers a record, executes a targeted `DELETE /usuarios/{id}`, and runs a subsequent `GET` check to confirm the profile is fully expunged.
* **Scenario 05 (Positive) `test_search_user_by_id`:** Asserts direct id-parameterized lookups via `GET /usuarios/{id}`, ensuring contract data integrity.
* **Scenario 06 (Positive) `test_update_user_successfully`:** Isolates state using randomized UUID structures, applies changes via an authorized `PUT /usuarios/{id}`, and confirms a `200 OK` update state.
* **Scenario 07 (Negative) `test_update_user_duplicated_email`:** Populates two separate users and attempts to overwrite the second profile's email parameter with the first user's registered address via a `PUT` mutation, forcing a `400 Bad Request` validation failure.

### Product Catalog Management (`/produtos`)
* **Scenario 01 (Positive) `test_create_product_successfully_with_admin_token`:** Registers an item via `POST /produtos` using administrative tokens, asserting a successful `200/201` status before cleaning the environment.
* **Scenario 02 (Negative/Security) `test_create_product_without_admin_token`:** Validates access control blockages by dropping auth headers on catalog insertions, confirming an explicit `401/403` handling.
* **Scenario 03 (Negative) `test_create_product_without_name`:** Drops the `nome` key from the payload dictionary via controlled fixture mutations, ensuring a `400 Bad Request` rejection.
* **Scenario 04 (Negative) `test_create_product_without_price`:** Drops the `preco` key from the payload dictionary via controlled fixture mutations, ensuring a `400 Bad Request` rejection.
* **Scenario 05 (Negative) `test_create_product_without_description`:** Drops the `descricao` key from the payload dictionary via controlled fixture mutations, ensuring a `400 Bad Request` rejection.
* **Scenario 06 (Positive) `test_search_product_by_id`:** Generates an isolated catalog listing, checks specific parameter lookups via `GET /produtos/{id}`, and cascades a deletion teardown.
* **Scenario 07 (Positive) `test_update_product_with_token`:** Creates a target resource and alters its properties using active admin authorization tokens via `PUT /produtos/{id}`.
* **Scenario 08 (Negative/Security) `test_update_product_without_token`:** Sets up a test item but strips the authorization header out of the subsequent `PUT` modification request, ensuring the API returns a proper `401/403` message block.
* **Scenario 09 (Positive) `test_delete_product_successfully`:** Seeds an item and verifies the behavior of administrative deletions using target endpoints.

### Shopping Carts & Checkout (`/carrinhos`)
* **Scenario 01 (Positive) `test_create_cart_successfully`:** Coordinates an upstream product setup, hooks the dynamic `idProduto` into a cart payload, asserts a `201 Created` status with schema validations, and applies a robust multi-tiered teardown process.
* **Scenario 02 (Negative) `test_create_cart_insufficient_stock`:** Provisions a product and intentionally leverages a `payload_factory` to ask for a volume of 50 units, asserting that the engine catches the stock deficit and throws a `400 Bad Request`.
* **Scenario 03 (Positive) `test_conclude_purchase_successfully`:** Mounts a valid card structure linked to an active product, calls `DELETE /carrinhos/concluir-compra`, and asserts a clean checkout completion (`200 OK`).
* **Scenario 04 (Positive) `test_cancel_purchase_and_stock_return`:** Builds a test state, hits the `/cancelar-compra` route, and validates that the system reverses the checkout, returns a `200 OK`, and automatically restocks the inventory pools.

---

## 5. Definition of Done (DoD)
A test script is only considered completed and eligible to be merged into the `main` branch when it satisfies the following validation gates:

1. **Triple Assertion Paradigm:** Every automation script must explicitly validate the HTTP **Status Code**, verify structural accuracy within the **Response Body** (error messages or payload payloads), and ensure acceptable server performance (Tolerable **Response Time**).
2. **State Independence:** Side effects from previous test execution blocks must never impact current tests. Pre-requisite data states must be generated and systematically destroyed dynamically using localized `pytest` fixtures.
3. **Strict Type Contracts:** Major mutations must pass strict JSON schema evaluation gates using `pytest-schema` to guarantee structural regressions do not go unnoticed.
4. **Isolated Docker Integrity:** The full suite must execute seamlessly and pass without local errors inside the project's specialized container.
5. **CI Pipeline Stability:** Remote pushes must trigger a green build across the sandboxed workflows defined in `.github/workflows/ci.yml`.