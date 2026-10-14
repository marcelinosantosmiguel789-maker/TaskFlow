from Domain.Entities.tarefa import Tarefa
from Domain.Interfaces.ITarefaRepository import ITarefaRepository

class CriarTarefa:
    def __init__(self, tarefa_repository: ITarefaRepository):
        self.tarefa_repository = tarefa_repository

    def criar(self, titulo: str, descricao: str, projeto_id: int):
        tarefa = Tarefa(id=None, titulo=titulo, descricao=descricao, concluida=False, projeto_id=projeto_id)
        return self.tarefa_repository.adicionar_tarefa(tarefa)
