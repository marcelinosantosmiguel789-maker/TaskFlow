class buscarProjeto:
    def __init__(self, projeto_repository):
        self.projeto_repository = projeto_repository
    
    def buscar(self, projeto_id: int):
        projeto = self.projeto_repository.buscar_projeto(projeto_id)
        return projeto