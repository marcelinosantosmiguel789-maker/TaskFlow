from abc import ABC, abstractmethod

class IProjetoRepository(ABC):
    @abstractmethod
    def create(self, projeto):
        pass

    @abstractmethod
    def read(self, id):
        pass

    @abstractmethod
    def update(self, projeto):
        pass

    @abstractmethod
    def delete(self, id):
        pass