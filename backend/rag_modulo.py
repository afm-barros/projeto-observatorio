import os
import psycopg2
from pgvector.psycopg2 import register_vector
from langchain_openai import OpenAIEmbeddings

# A chave vai aqui (mesmo que ainda não esteja ativa)
# os.environ["OPENAI_API_KEY"] = "sk-proj-..."

DB_URL = "postgresql://admin:adminpassword@localhost:5432/observatorio"

def get_connection():
    conn = psycopg2.connect(DB_URL)
    register_vector(conn)
    return conn

def gerar_embedding(texto: str):
    """
    Tenta usar a OpenAI. Se a chave estiver inativa, gera um vetor MOCK.
    """
    try:
        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
        return embeddings_model.embed_query(texto)
    except Exception as e:
        print(f"⚠️ Chave inativa ou erro na OpenAI. Gerando vetor falso para: {texto[:30]}...")
        # Retorna um vetor de 1536 dimensões preenchido com zeros (Mock)
        return [0.0] * 1536

def salvar_pesquisador_com_artigos(nome, classe, temas, citacoes, artigos):
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Salva o Pesquisador
    cursor.execute("""
        INSERT INTO pesquisadores (nome, classe, temas, citacoes)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (nome) DO NOTHING
        RETURNING id;
    """, (nome, classe, temas, citacoes))
    
    resultado = cursor.fetchone()
    if resultado:
        pesquisador_id = resultado[0]
    else:
        cursor.execute("SELECT id FROM pesquisadores WHERE nome = %s", (nome,))
        pesquisador_id = cursor.fetchone()[0]

    # 2. Salva as Produções
    for artigo in artigos:
        titulo = artigo.get("titulo", "")
        qualis = artigo.get("qualis", "N/A")
        
        cursor.execute("SELECT id FROM producoes WHERE titulo = %s", (titulo,))
        if cursor.fetchone():
            continue
            
        vetor = gerar_embedding(titulo)
        
        cursor.execute("""
            INSERT INTO producoes (pesquisador_id, titulo, qualis, embedding)
            VALUES (%s, %s, %s, %s);
        """, (pesquisador_id, titulo, qualis, vetor))
        
    conn.commit()
    cursor.close()
    conn.close()