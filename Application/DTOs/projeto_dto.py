from pydantic import BaseModel
from Domain.Entities.projeto import Projeto

class ProjetoDTO(BaseModel):
    id: int
    nome: str
    descricao: str | None

def mapear_projeto_para_dto(projeto: Projeto) -> ProjetoDTO:
    return ProjetoDTO(
        id=projeto.id,
        nome=projeto.nome,
        descricao=projeto.descricao
    )