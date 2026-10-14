from Domain.Entities.projeto import Projeto
from Domain.Interfaces.IProjetoRepository import IProjetoRepository

class criarProjeto:
    def __init__(self, projeto_repository: IProjetoRepository):
        self.projeto_repository = projeto_repository
    
    def criar(self, nome: str, descricao: str):
        projeto = Projeto(id=None, nome=nome, descricao=descricao)
        return self.projeto_repository.adicionar_projeto(projeto)