
from pydantic import BaseModel

from Domain.Entities.tarefa import Tarefa


class TarefaDTO(BaseModel):
    id: int
    titulo: str
    descricao: str
    concluida: bool


def mapear_tarefa_para_dto(tarefa: Tarefa) -> TarefaDTO:
    return TarefaDTO(
        id=tarefa.id,
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        concluida=(tarefa.status == "concluida")
    )
