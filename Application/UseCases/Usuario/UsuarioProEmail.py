from Domain.Entities.usuario import Usuario
from Infraestrcuture.Repositories.usuarioRepository import UsuarioRepository

class ObterUsuarioPorEmail:
    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    def obter_usuario_por_email(self, email: str) -> Usuario | None:
        return self.usuario_repository.obter_usuario_por_email(email)