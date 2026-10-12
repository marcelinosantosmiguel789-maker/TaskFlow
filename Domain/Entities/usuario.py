
class Usuario:
    def __init__(self, id: int, nome: str, email: str, senha: str):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    def validar_senha(self, senha: str) -> bool:
        return self.senha == senha

    def validar_email(self, email: str) -> bool:
        return self.email == email
