
from Domain.Services.password_hasher import verify_password


class Usuario:
    def __init__(
        self,
        id: int | None,
        nome: str,
        email: str,
        senha: str,
        ativo: bool = True,
    ):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo

    def validar_senha(self, senha: str) -> bool:
        return verify_password(senha, self.senha)

    def validar_email(self, email: str) -> bool:
        return self.email == email
