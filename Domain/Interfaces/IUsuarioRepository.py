from abc import ABC, abstractmethod

class ITarefaRepository(ABC):
    @abstractmethod
    def create(self, tarefa):
        pass

    @abstractmethod
    def read(self, id):
        pass

    @abstractmethod
    def update(self, tarefa):
        pass

    @abstractmethod
    def delete(self, id):
        pass