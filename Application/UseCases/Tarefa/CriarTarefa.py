from Domain.Entities.tarefa import Tarefa
from Domain.Exceptions import DadosInvalidosError
from Domain.Interfaces.ITarefaRepository import ITarefaRepository

class CriarTarefa:
    def __init__(self, tarefa_repository: ITarefaRepository):
        self.tarefa_repository = tarefa_repository

    def criar(
        self,
        titulo: str,
        descricao: str | None,
        projeto_id: int,
    ):
        if not isinstance(projeto_id, int) or projeto_id <= 0:
            raise DadosInvalidosError(
                "O ID do projeto deve ser um inteiro positivo."
            )
        titulo = titulo.strip()
        if not titulo:
            raise DadosInvalidosError("O título da tarefa é obrigatório.")
        if len(titulo) > 255:
            raise DadosInvalidosError("O título deve ter até 255 caracteres.")
        if descricao is not None and len(descricao) > 255:
            raise DadosInvalidosError("A descrição deve ter até 255 caracteres.")
        tarefa = Tarefa(
            id=None,
            titulo=titulo,
            descricao=descricao.strip() if descricao is not None else None,
            concluida=False,
            projeto_id=projeto_id,
        )
        return self.tarefa_repository.adicionar_tarefa(tarefa)
