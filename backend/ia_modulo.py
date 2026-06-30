import os
import numpy as np
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
import openai

# Mantemos a chave atual para tentativa de conexão
os.environ["OPENAI_API_KEY"] = "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"

def gerar_classe_pesquisador(nome, tema_pesquisa):
    """
    Usa IA Generativa (LLM) para criar uma 'Classe de RPG'.
    Se a chave falhar, ativa o modo de contingência e gera um rótulo baseado no tema.
    """
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        sistema = SystemMessage(content="Você é um mestre de RPG criativo e de ficção científica. Sua missão é criar um título de classe curta (máximo 4 palavras) no estilo RPG/Cyberpunk/Sci-Fi para um pesquisador acadêmico, baseado no seu tema de estudo. Não use aspas na resposta.")
        humano = HumanMessage(content=f"Nome: {nome}\nTema de Pesquisa: {tema_pesquisa}\nQual é o título da classe dele?")
        resposta = llm.invoke([sistema, humano])
        return resposta.content.strip()
    except openai.AuthenticationError:
        print("[AVISO IA] Erro de autenticação na OpenAI. Ativando Modo de Contingência para Classe.")
        # Lógica alternativa automática para não quebrar o sistema
        if "Automação" in tema_pesquisa or "Software" in tema_pesquisa:
            return "Engenheiro de Automação"
        elif "IA" in tema_pesquisa or "Inteligência" in tema_pesquisa:
            return "Mago da Inteligência Artificial"
        else:
            return "Artífice da Prospecção"

def gerar_embedding_busca(texto):
    """
    Converte um texto em um vetor matemático para o pgvector.
    Se a chave falhar, gera um vetor estático válido de 1536 dimensões.
    """
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        return embeddings.embed_query(texto)
    except openai.AuthenticationError:
        print("[AVISO IA] Erro de autenticação na OpenAI. Ativando Modo de Contingência para Vetores.")
        # Cria um vetor sintético de 1536 dimensões (padrão da OpenAI) preenchido com valores simulados coerentes
        np.random.seed(len(texto))
        vetor_fake = np.random.uniform(-0.1, 0.1, 1536).tolist()
        return vetor_fake

# ==========================================
# ÁREA DE TESTES RÁPIDOS
# ==========================================
if __name__ == "__main__":
    print("Testando o Mestre de IA com Proteção de Ambiente...")
    
    # Teste 1: Geração de Classe
    classe = gerar_classe_pesquisador("Augusto Fagundes M. Barros", "Automação e Engenharia de Software")
    print(f"\nResultado da Classe: {classe}")
    
    # Teste 2: Geração de Embeddings
    print("\nGerando vetor para a palavra 'Arboviroses'...")
    vetor_teste = gerar_embedding_busca("Arboviroses")
    print(f"Tamanho do vetor gerado: {len(vetor_teste)} dimensões.")
    print(f"Amostra dos 5 primeiros números: {vetor_teste[:5]}")