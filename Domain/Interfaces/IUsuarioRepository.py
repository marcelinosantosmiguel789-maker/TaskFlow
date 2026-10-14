from abc import ABC, abstractmethod


class IUsuarioRepository(ABC):
    @abstractmethod
    def adicionar_usuario(self, usuario):
        pass

    @abstractmethod
    def obter_usuario_por_email(self, email: str):
        pass