from Domain.Entities.projeto import Projeto
from Domain.Exceptions import DadosInvalidosError
from Domain.Interfaces.IProjetoRepository import IProjetoRepository

class criarProjeto:
    def __init__(self, projeto_repository: IProjetoRepository):
        self.projeto_repository = projeto_repository
    
    def criar(self, nome: str, descricao: str | None):
        nome = nome.strip()
        if not nome:
            raise DadosInvalidosError("O nome do projeto é obrigatório.")
        if len(nome) > 255:
            raise DadosInvalidosError(
                "O nome do projeto deve ter até 255 caracteres."
            )
        if descricao is not None and len(descricao) > 255:
            raise DadosInvalidosError("A descrição deve ter até 255 caracteres.")
        projeto = Projeto(
            id=None,
            nome=nome,
            descricao=descricao.strip() if descricao is not None else None,
        )
        return self.projeto_repository.adicionar_projeto(projeto)