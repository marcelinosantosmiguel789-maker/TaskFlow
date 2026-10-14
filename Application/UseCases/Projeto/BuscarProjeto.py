from Domain.Entities.projeto import Projeto
from Domain.Interfaces.IProjetoRepository import IProjetoRepository

class BuscarProjeto:
    def __init__(self, projeto_repository: IProjetoRepository):
        self.projeto_repository = projeto_repository

    def buscar_por_id(self, projeto_id: int) -> Projeto | None:
        return self.projeto_repository.obter_projeto_por_id(projeto_id)