from Domain.Exceptions import DadosInvalidosError
from Domain.Interfaces.ITarefaRepository import ITarefaRepository


class ExcluirTarefa:
    def __init__(self, tarefa_repository: ITarefaRepository):
        self.tarefa_repository = tarefa_repository

    def excluir(self, tarefa_id: int) -> bool:
        if tarefa_id <= 0:
            raise DadosInvalidosError(
                "O ID da tarefa deve ser um inteiro positivo."
            )
        return self.tarefa_repository.excluir_tarefa(tarefa_id)
