from Domain.Exceptions import DadosInvalidosError
from Domain.Interfaces.IProjetoRepository import IProjetoRepository


class AtualizarProjeto:
    def __init__(self, projeto_repository: IProjetoRepository):
        self.projeto_repository = projeto_repository

    def atualizar(self, projeto_id: int, dados: dict):
        if projeto_id <= 0:
            raise DadosInvalidosError(
                "O ID do projeto deve ser um inteiro positivo."
            )
        dados = dict(dados)
        if "nome" in dados:
            dados["nome"] = dados["nome"].strip()
            if not dados["nome"]:
                raise DadosInvalidosError("O nome do projeto é obrigatório.")
            if len(dados["nome"]) > 255:
                raise DadosInvalidosError(
                    "O nome do projeto deve ter até 255 caracteres."
                )
        if "descricao" in dados and dados["descricao"] is not None:
            dados["descricao"] = dados["descricao"].strip()
            if len(dados["descricao"]) > 255:
                raise DadosInvalidosError(
                    "A descrição deve ter até 255 caracteres."
                )
        return self.projeto_repository.atualizar_projeto(projeto_id, dados)
