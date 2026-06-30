from pydantic import BaseModel, Field
from typing import Optional

class Pesquisador(BaseModel):
    # Lattes corrigido para exigir exatamente 16 dígitos numéricos
    lattes_id: str = Field(..., min_length=16, max_length=16) 
    
    # Nome mantido como estava
    nome: str = Field(..., min_length=2, max_length=70)
    
    # ID corrigido para Inteiro, sem limite de caracteres (pois o banco controla isso)
    pesquisadores_id: Optional[int] = Field(default=None)