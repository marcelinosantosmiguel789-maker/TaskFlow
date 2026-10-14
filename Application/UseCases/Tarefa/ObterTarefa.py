from Domain.Entities.tarefa import Tarefa
from Infraestrcuture.databases.tarefa_model import TarefaModel

class ObterTarefa:
    def __init__(self, tarefa_repository):
        self.tarefa_repository = tarefa_repository

    def obter_por_projeto(self, projeto_id: int):
        tarefas = self.tarefa_repository.obter_tarefas_por_projeto(projeto_id)
        return tarefas