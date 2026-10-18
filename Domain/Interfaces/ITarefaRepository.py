from abc import ABC, abstractmethod


class ITarefaRepository(ABC):
    @abstractmethod
    def adicionar_tarefa(self, tarefa):
        pass

    @abstractmethod
    def obter_tarefas_por_projeto(self, projeto_id: int):
        pass

    @abstractmethod
    def obter_tarefa_por_id(self, tarefa_id: int):
        pass

    @abstractmethod
    def atualizar_tarefa(self, tarefa_id: int, dados: dict):
        pass

    @abstractmethod
    def excluir_tarefa(self, tarefa_id: int):
        pass