from Domain.Exceptions import DadosInvalidosError
from Domain.Interfaces.ITarefaRepository import ITarefaRepository


class AtualizarTarefa:
    def __init__(self, tarefa_repository: ITarefaRepository):
        self.tarefa_repository = tarefa_repository

    def atualizar(self, tarefa_id: int, dados: dict):
        if tarefa_id <= 0:
            raise DadosInvalidosError(
                "O ID da tarefa deve ser um inteiro positivo."
            )
        dados = dict(dados)
        if "titulo" in dados:
            dados["titulo"] = dados["titulo"].strip()
            if not dados["titulo"]:
                raise DadosInvalidosError("O título da tarefa é obrigatório.")
            if len(dados["titulo"]) > 255:
                raise DadosInvalidosError(
                    "O título deve ter até 255 caracteres."
                )
        if "descricao" in dados and dados["descricao"] is not None:
            dados["descricao"] = dados["descricao"].strip()
            if len(dados["descricao"]) > 255:
                raise DadosInvalidosError(
                    "A descrição deve ter até 255 caracteres."
                )
        return self.tarefa_repository.atualizar_tarefa(tarefa_id, dados)
