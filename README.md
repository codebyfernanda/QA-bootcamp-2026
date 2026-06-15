# Desafio Técnico | Bootcamp AWS AI FDE Driven Quality Engineering 

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pytest-9.0-0A9EDC?logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/Coverage-100%25-brightgreen" />
  <img src="https://img.shields.io/badge/Status-Finalizado-success" />
</p>

Este projeto consiste em uma suíte de testes automatizados desenvolvida em **Python**, utilizando o framework **Pytest**. O objetivo principal é validar as regras de negócio e os contratos dos endpoints de *Usuários*, *Produtos*, *Login* e *Carrinhos* da API pública [**ServeRest**](https://compassuol.serverest.dev/?lang=pt-BR#/), garantindo a integridade das informações, a resiliência do sistema e a exatidão das respostas.

---

## Evolução da Arquitetura e Refatoração (Semana 04)

Durante a [quarta semana](https://github.com/codebyfernanda/bootcamp-QA-2026-desafios/tree/main/semana_004) do Bootcamp, a arquitetura do projeto foi refatorada seguindo as melhores práticas de Engenharia de Qualidade para eliminar gargalos de manutenção e melhorar a legibilidade do código:

* **Modularização por Domínio de Negócio:** Reorganização dos arquivos de teste em módulos claros por contexto (Login, Usuários, Produtos e Carrinhos), abandonando abordagens monolíticas.
* **Adoção do Padrão AAA (Arrange, Act, Assert):** Remoção de blocos redundantes de `try/except` que poluíam o código. A estrutura agora segue rigorosamente o fluxo de *Organizar, Agir e Validar*, tornando os testes focados e legíveis.
* **Centralização da Base URL:** Criação de *fixtures* dedicadas para gerenciar a URL base da API, eliminando a repetição de strings nos testes e facilitando a transição entre diferentes ambientes de teste.
* **Gestão de Estado (Setup/Teardown):** Implementação de rotinas automatizadas de limpeza da base de dados (`teardown`), garantindo a independência entre os cenários.
* **Testes de Contrato (Contract Testing):** Evolução das validações simples de `status_code` e chaves isoladas para uma validação estrutural completa do payload de resposta, utilizando a biblioteca `jsonschema`.

---

# Plano de Testes: Detalhamento do Projeto

<details>
<summary><b>1. Objetivo e Estratégia</b></summary>

* **Objetivo:** Assegurar a qualidade funcional, estabilidade de contrato e confiabilidade dos principais fluxos de negócio da API ServeRest.
* **Estratégia:** Automação de testes funcionais e de contrato na camada de Back-end (API).
* **Stack Tecnológica:** Python 3.13.x, Pytest, Requests e JSONSchema.
* **Escopo Coberto:** Endpoints `/login`, `/usuarios`, `/produtos` e `/carrinhos`.
* **Fora de Escopo:** Testes de carga, estresse e performance.
</details>

<details>
<summary><b>2. Cenários de Teste Mapeados</b></summary>

* **`test_login.py`**: Suíte de autenticação abrangendo cenários de sucesso e falhas por campos ausentes ou dados inválidos.
* **`test_usuarios.py`**: CRUD completo (POST, GET, PUT, DELETE) com validações de e-mail duplicado e integridade de dados.
* **`test_produtos.py`**: CRUD de produtos com validação de tokens de administrador e restrições de campos obrigatórios.
* **`test_carrinhos.py`**: Gestão de compras, incluindo estoques insuficientes e cancelamento de pedidos com retorno de estoque.
</details>

<details>
<summary><b>3. Definition of Done (DoD)</b></summary>

Para garantir o padrão de qualidade, cada teste deve atender aos critérios:
- [x] Nomenclatura padronizada: `test_<action>_<expected_result>`.
- [x] *Fixtures* centralizadas (`conftest.py`).
- [x] Massa de dados dinâmica (UUID).
- [x] Validação estrutural completa via `JSON Schema`.
</details>

## Estrutura do Projeto 

```text
├── tests/              
│   ├── conftest.py         # Configurações globais e fixtures
│   ├── schemas.py          # Definições de JSON Schemas
│   ├── test_login.py       # Testes de autenticação
│   ├── test_produtos.py    # Testes do módulo de produtos
│   ├── test_usuarios.py    # Testes do módulo de usuários
│   └── test_carrinhos.py   # Testes do módulo de carrinhos

```
--- 

# Métricas e Resultados

## Cobertura de Testes (Test Coverage)

Para garantir a robustez e a qualidade da API, a estratégia de automação foi baseada na metodologia de **Operator Coverage**, que mede a abrangência dos métodos HTTP testados em relação aos endpoints disponíveis.

### Mapa de Cobertura de Operações

| Endpoint | POST | GET | PUT | DELETE | Total de Operações |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `/login` | ✅ | - | - | - | 1 |
| `/usuarios` | ✅ | ✅ | ✅ | ✅ | 4 |
| `/produtos` | ✅ | ✅ | ✅ | ✅ | 4 |
| `/carrinhos` | ✅ | - | - | ✅ | 2 |
| **Totais** | **4** | **2** | **2** | **3** | **11 / 11** |

### Metodologia de Cálculo
O cálculo foi realizado através da fórmula de *Operator Coverage*:

Como a API expõe 11 operações distintas entre os quatro recursos (Login, Usuários, Produtos e Carrinhos) e todos os fluxos foram devidamente automatizados, a suíte alcançou **100% de cobertura de operações**.

---
## Qualidade Além da Cobertura
Além de atingir 100% de cobertura de operadores, a suíte foca na **qualidade das validações**:

* **Status Code Coverage:** Validação de fluxos de sucesso (200, 201) e cenários de erro esperados (400, 401, 403, 404).
* **JSON Schema Validation:** Garantia de que o contrato da API está sendo respeitado em cada resposta, assegurando que o Front-End receba os dados esperados.
* **Fluxo de Integração:** Testes que orquestram dependências, como a criação de um produto para uso posterior na criação de um carrinho, simulando o uso real do sistema.

--- 

### Bugs e Inconsistência Encontradas

| Severidade | Bug / Inconsistência | Comportamento Esperado | Comportamento Obtido |
| --- | --- | --- | --- |
| 🔴 **Crítica** | **Elevação de Privilégio** | O sistema deve impedir que um usuário comum altere seu perfil para `administrador: true`. | O `PUT /usuarios/{id}` aceita a alteração, promovendo o usuário a administrador. |
| 🔵 **Baixa** | **Inconsistência de Resposta (Payload Vazio)** | Retornar erro de validação padronizado (`400`) em todas as rotas ao receber `{}`. | Retorna `400` em rotas públicas e `401` em rotas privadas para o mesmo payload. |

---

## Principais Desafios e Aprendizados

| Desafio | Solução Encontrada |
| :--- | :--- |
| **Validação de Contratos (JSON Schema)** | Mapeamento das chaves de erro específicas por campo (ex: `"nome": "nome é obrigatório"`) em vez de chaves genéricas, facilitando o tratamento de erros no Front-End. |
| **Retorno de Verbos HTTP** | Separação estratégica entre *Schemas* de mutação (apenas `message` e `_id`) e *Schemas* de leitura (objeto completo), ajustando as expectativas das validações. |
| **Encadeamento de Requisições** | Implementação de fluxos encadeados (POST Produto > Extração de `_id` > Montagem de Payload > POST Carrinho) para respeitar a arquitetura relacional da API. |
| **Mutabilidade de Dados** | Utilização do método `.copy()` em dicionários para evitar que a manipulação de dados em um teste afetasse o estado original da *fixture* nos testes subsequentes. |
| **Rigor do Pytest (Nomenclatura)** | Desenvolvimento de leitura crítica dos logs de erro do Pytest para identificar rapidamente desvios de nomenclatura entre fixtures e parâmetros injetados. |
| **Ambiente de Desenvolvimento** | Reforço da atenção aos indicadores visuais de salvamento de arquivos no VS Code, eliminando falsos positivos causados por execução de código desatualizado. |

---

## Conclusão

O desafio foi um verdadeiro mergulho no que significa, na prática, ser uma Eng. de Qualidade. Conforme o nosso instrutor Jacques Schmitz comentou no nosso 1º Workshop, **"o QA atua em todo o ciclo, como facilitador na vida do time que pode influenciar no design, auxiliar na observabilidade e na questão de como lidar com a massa de dados obtida pelo negócio"**. Entendi que, quando estruturamos testes bem organizados, a missão não é somente encontrar bug mas prevenir que problemas apareçam, ao mesmo tempo que reduz riscos para o negócio. 

Muito além de apenas automatizar o trabalho manual, estamos construindo uma camada de segurança "para ter tranquilidade e segurança com as mudanças" e "garantir que as mudanças não quebrem outros aspectos do código", é o que afirmou o prof. José Correia, Especialista em Qualidade de Software, no curso Início Rápido em Teste e QA, disponível na Udemy (que estudamos durante a primeira semana de estudos no Bootcamp).

A refatoração que realizei nesta quarta semana me trouxe um insight valioso: **qualidade é parte intrínseca da arquitetura e, nós, como QA, devemos atuar em todo o ciclo da aplicação** (conforme indicado pelo raciocínio shift-left), tal questão foi perguntada no nosso Questionário da segunda semana de estudos. Quando tratamos os contratos de API com o mesmo cuidado que tratamos a interface do usuário, fazemos com que todos enxerguem "que qualidade é um esforço de time e importante para o produto", conceito trabalhado por Correia. 

Dessa forma, garantimos que o ecossistema inteiro fale a mesma língua. **E pensando em toda essa experiência: Sigo ainda mais motivada e com a bagagem reforçada para aplicar essa visão estratégica em cenários de negócios, exercendo o papel de um membro ativo do projeto que trabalha para aconselhar sobre qualidade.**

---

## Referências Utilizadas em Consultas

* [AAA Pattern in Test Automation - Semaphore CI](https://semaphore.io/blog/aaa-pattern-test-automation)
* [Pytest Documentation & Best Practices](https://docs.pytest.org/)
* [Pytest: Help your tests do more](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
* [Como verificar a cobertura de testes de APIs REST](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b)
* [Test Coverage Criteria for RESTful Web APIs](https://www.researchgate.net/publication/327774902_Test_coverage_criteria_for_RESTful_web_APIs) 
* [Introduction to Contract Testing](https://martinfowler.com/articles/contract-testing.html)
* [Understanding JSON Schema](https://json-schema.org/learn/getting-started-step-by-step) 

---

### Como Executar este Repositório

1. **Clone o repositório:**
```bash
git clone <https://github.com/codebyfernanda/bootcamp-QA-2026-desafios.git>
cd bootcamp-QA-2026-desafios

```

2. **Crie e ative um ambiente virtual:**

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

3. **Instale as dependências:**

```bash
pip install -r requirements.txt

```

4. **Execute os testes:**

```bash
pytest -v

```
---


## Sobre a Autora

O presente projeto foi desenvolvido por **Fernanda Bastos dos Santos** [(@codebyfernanda)](https://github.com/codebyfernanda), estudante de **Análise e Desenvolvimento de Sistemas** no Mackenzie, durante o **BOOTCAMP | AWS AI FDE DRIVEN QUALITY ENGINEERING**, da Compass UOL com [AI/R Company](https://aircompany.ai/).

## Agradecimentos Especiais

Gostaria de expressar meus agradecimentos à Squad 2 pelo engajamento, por toda troca de conhecimento e, também, pelo suporte durante o processo do nosso Bootcamp. Deixo aqui um agradecimento especial aos meus colegas [Renan Pacheco](https://github.com/Renanpacheco) e [Vitor Kunicki](https://github.com/vitto2099). A paciência, a disponibilidade e o auxílio de vocês foram fundamentais para a superação dos desafios dessa entrega. 

Também gostaria de aproveitar este espaço para registrar os meus agradecimentos aos meus instrutores, Amanda Almeida e [Jacques Schmitz](https://github.com/juniorschmitz), pelo apoio contínuo e a disponibilidade para auxiliar com conteúdos técnicos na formação, e à Scrum Master Leticia Souza, pelo acompanhamento diário e sensibilidade com a nossa trajetória no programa. Muito obrigada! :)
