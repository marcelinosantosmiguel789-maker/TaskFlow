from Domain.Entities.usuario import Usuario
from Infraestrcuture.Repositories.usuarioRepository import UsuarioRepository

class CriarUsuario:
    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    def criar_usuario(self, nome: str, email: str, senha: str) -> int:
        usuario = Usuario(id=None, nome=nome, email=email, senha=senha, ativo=True)
        return self.usuario_repository.adicionar_usuario(usuario)
