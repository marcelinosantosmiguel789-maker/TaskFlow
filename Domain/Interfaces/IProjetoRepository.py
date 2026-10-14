from abc import ABC, abstractmethod


class IProjetoRepository(ABC):
    @abstractmethod
    def adicionar_projeto(self, projeto):
        pass

    @abstractmethod
    def obter_projeto_por_id(self, projeto_id: int):
        pass

    @abstractmethod
    def listar_projetos(self):
        pass