from Domain.Entities.usuario import Usuario
from Domain.Interfaces.IUsuarioRepository import IUsuarioRepository
from Domain.Services.password_hasher import hash_password

class CriarUsuario:
    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository

    def criar_usuario(self, nome: str, email: str, senha: str) -> int:
        senha_hash = hash_password(senha)
        usuario = Usuario(id=None, nome=nome, email=email, senha=senha_hash, ativo=True)
        return self.usuario_repository.adicionar_usuario(usuario)
