from Domain.Entities.usuario import Usuario
from Domain.Exceptions import DadosInvalidosError
from Domain.Interfaces.IUsuarioRepository import IUsuarioRepository
from Domain.Services.password_hasher import hash_password

class CriarUsuario:
    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository

    def criar_usuario(self, nome: str, email: str, senha: str) -> int:
        nome = nome.strip()
        email = email.strip().lower()
        if not nome:
            raise DadosInvalidosError("O nome do usuário é obrigatório.")
        if len(nome) > 255:
            raise DadosInvalidosError(
                "O nome do usuário deve ter até 255 caracteres."
            )
        if not email:
            raise DadosInvalidosError("O e-mail do usuário é obrigatório.")
        if not senha.strip():
            raise DadosInvalidosError("A senha do usuário é obrigatória.")
        senha_hash = hash_password(senha)
        usuario = Usuario(id=None, nome=nome, email=email, senha=senha_hash, ativo=True)
        return self.usuario_repository.adicionar_usuario(usuario)
