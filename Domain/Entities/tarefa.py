class Tarefa:
    def __init__(
        self,
        id: int | None,
        titulo: str,
        descricao: str | None,
        concluida: bool,
        projeto_id: int,
    ):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.concluida = concluida
        self.projeto_id = projeto_id