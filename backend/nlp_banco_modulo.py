import sqlite3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

# Baixa os pacotes necessários do NLTK silenciosamente na primeira vez
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# 1. FUNÇÃO NLTK: Limpa os temas usando Processamento de Linguagem Natural
def processar_temas_nltk(temas_lista):
    """
    Usa NLTK para tokenizar e remover stopwords dos temas do OpenAlex,
    garantindo que tenhamos apenas as palavras de maior peso semântico.
    """
    if not temas_lista:
        return ["Erudição"]
        
    texto_completo = " ".join(temas_lista).lower()
    
    # Tokenização (NLTK)
    tokens = word_tokenize(texto_completo)
    
    # Remoção de Stopwords (Inglês e Português) (NLTK)
    stop_words_pt = set(stopwords.words('portuguese'))
    stop_words_en = set(stopwords.words('english'))
    
    tags_limpas = [
        palavra for palavra in tokens 
        if palavra.isalpha() and palavra not in stop_words_pt and palavra not in stop_words_en
    ]
    
    # Retorna as palavras únicas extraídas
    return list(set(tags_limpas))[:4] # Pega até 4 palavras-chave limpas


# 2. FUNÇÃO FTS: Cria o banco e salva o histórico
def salvar_no_grimorio_fts(nome, classe, temas, citacoes):
    """
    Salva o pesquisador em um banco SQLite usando FTS5 para buscas ultrarrápidas.
    Isso atende ao requisito de usar Full-Text Search.
    """
    db_path = 'grimorio_local.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Cria a tabela virtual FTS5 se não existir
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS pesquisadores_fts 
        USING fts5(nome, classe, temas, citacoes)
    ''')
    
    temas_str = ", ".join(temas)
    
    # Verifica se já existe para não duplicar (busca rápida)
    cursor.execute("SELECT * FROM pesquisadores_fts WHERE nome MATCH ?", (f'"{nome}"',))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO pesquisadores_fts (nome, classe, temas, citacoes)
            VALUES (?, ?, ?, ?)
        ''', (nome, classe, temas_str, str(citacoes)))
        conn.commit()
        
    conn.close()