class Projeto:
    def __init__(
        self,
        id: int | None,
        nome: str,
        descricao: str | None,
    ):
        self.id = id
        self.nome = nome
        self.descricao = descricao