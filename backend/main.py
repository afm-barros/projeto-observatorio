from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Importando todos os nossos pilares
from ia_modulo import gerar_classe_pesquisador
from openalex_modulo import buscar_pesquisadores_openalex
from nlp_banco_modulo import processar_temas_nltk, salvar_no_grimorio_fts
from rag_modulo import salvar_pesquisador_com_artigos # <-- O NOVO PILAR

app = FastAPI(title="API Observatório de Talentos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class BuscaRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Motor de Busca do Observatório operante!"}

@app.post("/buscar-pesquisadores")
def buscar_pesquisadores(request: BuscaRequest):
    lista_pesquisadores = buscar_pesquisadores_openalex(request.query)
    
    if not lista_pesquisadores:
        return {"status": "vazio", "resultados": []}
    
    for index, pesquisador in enumerate(lista_pesquisadores):
        tema_principal = pesquisador["temas"][0] if pesquisador["temas"] else "Pesquisa"
        
        # 1. NLP (NLTK) - Limpeza de Tags
        tags_nlp = processar_temas_nltk(pesquisador["temas"])
        pesquisador["temas"] = tags_nlp if tags_nlp else pesquisador["temas"]
        
        # 2. IA (LLM) - Geração da Classe RPG
        if index == 0:
            try:
                classe = gerar_classe_pesquisador(pesquisador["nome"], tema_principal)
                pesquisador["classe_criativa"] = classe
            except:
                pesquisador["classe_criativa"] = f"Mestre da Ordem de {tema_principal}"
        else:
            pesquisador["classe_criativa"] = f"Erudito em {tema_principal}"
            
        # 3. FTS (SQLite) - Cache Rápido Local
        salvar_no_grimorio_fts(
            nome=pesquisador["nome"], 
            classe=pesquisador["classe_criativa"], 
            temas=pesquisador["temas"],
            citacoes=pesquisador["total_citacoes"]
        )
        
        # 4. RAG & VETORES (PostgreSQL + pgvector) - O Cérebro Exigido pelo PDF
        if "artigos" in pesquisador and pesquisador["artigos"]:
            salvar_pesquisador_com_artigos(
                nome=pesquisador["nome"],
                classe=pesquisador["classe_criativa"],
                temas=", ".join(pesquisador["temas"]),
                citacoes=pesquisador["total_citacoes"],
                artigos=pesquisador["artigos"]
            )
            
    return {
        "status": "sucesso",
        "resultados": lista_pesquisadores
    }