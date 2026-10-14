from Domain.Entities.projeto import Projeto
from Infraestrcuture.databases import projeto_model
from Infraestrcuture.databases.projeto_model import ProjetoModel


class projetoRepository:
    def __init__(self, session):
        self.session = session

    def adicionar_projeto(self, projeto: Projeto):
        projeto_model = ProjetoModel(
            nome=projeto.nome,
            descricao=projeto.descricao
        )
        self.session.add(projeto_model)
        self.session.commit()
        return projeto_model.id

    def listar_projetos(self):
        projetos_model = self.session.query(ProjetoModel).all()
        return [Projeto(
            id=projeto.id,
            nome=projeto.nome,
            descricao=projeto.descricao
        ) for projeto in projetos_model]