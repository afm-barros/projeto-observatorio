from pydantic import BaseModel, Field
from typing import Optional

class Producao(BaseModel):
    # O ID da produção gerado pelo banco é um número inteiro
    id: Optional[int] = Field(default=None) 
    
    # A chave estrangeira que liga ao pesquisador também é um número inteiro (ex: 1 para Eduardo)
    pesquisador_id: int 
    
    # O nome do artigo continua como string, exigindo pelo menos 2 caracteres
    nomeartigo: str = Field(..., min_length=2)