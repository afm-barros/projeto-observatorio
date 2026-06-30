# Observatório de Dados Científicos da Bahia 🔬

Este repositório contém a infraestrutura de dados e a API Backend desenvolvidas para o projeto do Observatório de Dados Públicos de Ciência e Tecnologia da Bahia (UESC). O foco desta arquitetura é o processamento, armazenamento e disponibilização otimizada de dados de produções científicas extraídas da Plataforma Lattes.

## 🚀 Arquitetura e Tecnologias Aplicadas

A solução foi construída utilizando práticas modernas de Engenharia de Software, separando as responsabilidades em camadas distintas:

*   **Banco de Dados (PostgreSQL):** Implementação de busca semântica inteligente utilizando **Full Text Search (FTS)** nativo do PostgreSQL com **Índices GIN** e colunas vetoriais (`tsvector`), garantindo altíssima performance em queries complexas.
*   **Processamento de Linguagem Natural (Python & NLTK):** Scripts de sanitização de dados que aplicam técnicas de NLP, incluindo *Tokenização*, remoção de *Stop Words* e *Stemming* (redução ao radical) para otimizar os motores de busca.
*   **API RESTful (FastAPI):** Back-end construído no padrão **MVC** utilizando injeção de dependências (DAO). A API expõe rotas seguras e tipadas via **Pydantic**, com documentação automática gerada pelo Swagger UI (OpenAPI).

## 🛠️ Funcionalidades da API (CRUD)

A API fornece endpoints completos para o gerenciamento de **Pesquisadores** e de suas respectivas **Produções Científicas**, incluindo rotas parametrizadas para cruzamento de dados:

*   `GET /pesquisadores`
*   `POST /producoes`
*   `GET /pesquisadores/{pesquisador_id}/producoes` (Listagem específica)

## 📄 Artigos e Documentação

Para um aprofundamento técnico sobre as decisões de arquitetura e implementação do código deste repositório, confira os artigos publicados:

*   🔗 [Como Estender uma API FastAPI: Adicionando o CRUD de Produções](https://www.linkedin.com/pulse/como-estender-uma-api-fastapi-adicionando-o-crud-de-produ%C3%A7%C3%B5es-barros-cptaf)
