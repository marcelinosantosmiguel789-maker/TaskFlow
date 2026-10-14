from Domain.Interfaces.ITarefaRepository import ITarefaRepository

class ObterTarefa:
    def __init__(self, tarefa_repository: ITarefaRepository):
        self.tarefa_repository = tarefa_repository

    def obter_por_projeto(self, projeto_id: int):
        tarefas = self.tarefa_repository.obter_tarefas_por_projeto(projeto_id)
        return tarefas