from abc import ABC, abstractmethod


class ITarefaRepository(ABC):
    @abstractmethod
    def adicionar_tarefa(self, tarefa):
        pass

    @abstractmethod
    def obter_tarefas_por_projeto(self, projeto_id: int):
        pass