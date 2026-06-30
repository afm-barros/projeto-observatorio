from pydantic import BaseModel, Field
from typing import Optional

class Producao(BaseModel):
    # Usando Optional para o ID pois na hora de criar (POST) o banco pode gerar isso automaticamente
    id: Optional[str] = Field(None, min_length=36, max_length=36) 
    pesquisador_id: str = Field(..., min_length=36, max_length=36)
    nomeartigo: str = Field(..., min_length=2)