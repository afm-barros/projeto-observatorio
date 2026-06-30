import psycopg2
from pgvector.psycopg2 import register_vector
import os

DB_URL = "postgresql://admin:adminpassword@localhost:5432/observatorio"

def get_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

def inicializar_banco():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ativa a extensão exigida pelo professor
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    
    # Cria a tabela de Pesquisadores (CRUD)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pesquisadores (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) UNIQUE,
            classe VARCHAR(100),
            temas TEXT,
            citacoes INTEGER
        );
    """)
    
    # Cria a tabela de Produções (Artigos) com o campo embedding (vetor)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producoes (
            id SERIAL PRIMARY KEY,
            pesquisador_id INTEGER REFERENCES pesquisadores(id),
            titulo TEXT,
            qualis VARCHAR(10),
            jcr VARCHAR(20),
            embedding VECTOR(1536) -- Tamanho do vetor da OpenAI
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Banco PostgreSQL e pgvector inicializados com sucesso!")

if __name__ == "__main__":
    inicializar_banco()