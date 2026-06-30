<<<<<<< HEAD
# Tutorial com Flask e PostgreSQL

Esse tutorial mostra como fazer funcionar um crud simples usando a arquitetura MVC com Singleton.
Detalhes não são explicados pois não caberia aqui, mas o código está comentado.

As pastas estão organizadas de acordo com a responsabilidade de cada módulo.

- Na pasta controller há somente arquivos relacionados com os controladores. Já que temos apenas o pesquisador como entidade nesse tutorial, temos somente controladores relacionados com ele.
- Dentro da pasta controller também tem a pasta dao (Data Access Object), que tem somente código relacionado com a interação com o banco de dados.
- Na pasta model temos a classe da entidade Pesquisador

---

> [!IMPORTANT]
>
> Antes de começar verifique se você tem a versão do Python igual ou maior que a 3.12 e o Docker instalado. Você pode instalar no ambiente virtual, se preferir. Este tutorial não cobre a instalação do Python e suas dependências, pois os comandos podem ser diferentes dependendo da instalação.

### Passo 1

Rode o comando **git clone <endereco_do_repositorio>** na pasta desejada

### Passo 2

Crie um ambiente virtual python para não misturar as dependências desse tutorial com as bibliotecas instaladas globalmente no computador.

`python -m venv <nome_do_venv>`

ou

`python3 -m venv <nome_do_venv>`

Vai depender da sua instalação do python.

### Passo 3

Depois de criar o ambiente virtual, rode o seguinte comando no terminal:

##### No Linux

`source nome_do_ambiente/bin/activate`

##### No Windows

`nome_do_ambiente\Scripts\activate`

Após isso, entre na pasta do tutorial e rode `pip install -r requirements.txt` com o ambiente virtual ativado para instalar as dependências.

### Passo 4

Na raiz da aplicação, digite `docker-compose up` para subir o banco de dados pelo docker.
Depois rode o arquivo `povoar_bd.py` na pasta **banco** para colocar os dados dos pesquisadores para teste no banco.

### Passo 5

Rode o arquivo `app.py` e faça as requisições GET, POST, PUT e DELETE para **/pesquisadores** para testar.
A aplicação estará rodando na porta 8000. Digite `http://localhost:8000` no navegador.

Use o comando para rodar a aplicação:

`uvicorn app:app --reload`

O primeiro **app** em "app:app --reload" se refere ao nome do arquivo principal. Portanto, se seu arquivo estivesse como 'main', você usaria "main:app --reload".

---

> [!TIP]
>
> Caso queira refazer tudo de novo, há um arquivo `apagar_db.py` na pasta **banco**. Basta rodar ele com o banco de dados funcionando, mas com o `app.py` parado.
=======
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
>>>>>>> b61c7fcb1ade9679d2c008d11f5a26a290ff0ce2
