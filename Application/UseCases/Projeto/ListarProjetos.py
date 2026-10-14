from Domain.Interfaces.IProjetoRepository import IProjetoRepository

class listarProjetos:
    def __init__(self, projeto_repository: IProjetoRepository):
        self.projeto_repository = projeto_repository
    
    def listar(self):
        projetos = self.projeto_repository.listar_projetos()
        return projetos
    