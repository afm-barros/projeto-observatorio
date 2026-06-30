# Use a imagem oficial do pgvector
FROM pgvector/pgvector:pg17

# Variaveis de ambiente para o PostgreSQL
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=qualquer_uma
ENV POSTGRES_DB=BD_PESQUISADOR
ENV POSTGRES_HOST_AUTH_METHOD=trust
