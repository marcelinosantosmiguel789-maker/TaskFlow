from Domain.Entities.projeto import Projeto

class criarProjeto:
    def __init__(self, projeto_repository):
        self.projeto_repository = projeto_repository
    
    def criar(self, nome: str, descricao: str):
        projeto = Projeto(id=None, nome=nome, descricao=descricao)
        return self.projeto_repository.salvar_projeto(projeto)