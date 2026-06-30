# controller/producao_controller.py
from fastapi import APIRouter, HTTPException
from typing import List
from model.producao import Producao

# Vamos importar as funções do DAO que farão as consultas reais no banco
from controller.dao.producao_dao import (
    apagar_por_id,
    listar_todas,
    salvar_nova_producao,
    atualizar_por_id,
    listar_por_pesquisador # A exigência do PDF!
)

producao_router = APIRouter()

# Rota para salvar uma nova produção
@producao_router.post("/producoes", response_model=Producao)
def adicionar(producao: Producao):
    resposta = salvar_nova_producao(
        id=producao.id,
        pesquisador_id=producao.pesquisador_id,
        nomeartigo=producao.nomeartigo
    )
    
    if 'Erro' in resposta:
        raise HTTPException(status_code=400, detail=resposta)
    
    return producao

# Rota para listar todas as produções gerais
@producao_router.get("/producoes", response_model=List[Producao])
def listar():
    producoes = listar_todas()
    return producoes

# Rota ESPECÍFICA para listar as produções de UM pesquisador (Exigência do Projeto)
@producao_router.get("/pesquisadores/{pesquisador_id}/producoes", response_model=List[Producao])
def listar_producoes_do_pesquisador(pesquisador_id: str):
    producoes = listar_por_pesquisador(pesquisador_id)
    return producoes

# Rota para apagar uma produção
@producao_router.delete("/producoes/{id}", response_model=str)
def apagar(id: str):
    resposta = apagar_por_id(id)
    
    if 'inválido' in resposta or 'Erro' in resposta:
        raise HTTPException(status_code=400, detail=resposta)
    
    return resposta

# Rota para atualizar uma produção
@producao_router.put("/producoes/{id}", response_model=Producao)
def atualizar(id: str, producao: Producao):
    resposta = atualizar_por_id(
        id=id,
        pesquisador_id=producao.pesquisador_id,
        nomeartigo=producao.nomeartigo
    )
    
    if 'Erro' in resposta:
        raise HTTPException(status_code=400, detail=resposta)
    
    return producao