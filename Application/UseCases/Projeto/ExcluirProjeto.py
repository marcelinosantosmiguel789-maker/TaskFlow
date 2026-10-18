from Domain.Exceptions import DadosInvalidosError
from Domain.Interfaces.IProjetoRepository import IProjetoRepository


class ExcluirProjeto:
    def __init__(self, projeto_repository: IProjetoRepository):
        self.projeto_repository = projeto_repository

    def excluir(self, projeto_id: int) -> bool:
        if projeto_id <= 0:
            raise DadosInvalidosError(
                "O ID do projeto deve ser um inteiro positivo."
            )
        return self.projeto_repository.excluir_projeto(projeto_id)
