from Domain.Entities.usuario import Usuario
from Domain.Interfaces.IUsuarioRepository import IUsuarioRepository

class ObterUsuarioPorEmail:
    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository

    def obter_usuario_por_email(self, email: str) -> Usuario | None:
        return self.usuario_repository.obter_usuario_por_email(email)