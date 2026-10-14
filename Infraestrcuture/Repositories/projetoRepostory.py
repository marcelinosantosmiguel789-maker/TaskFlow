from Domain.Entities.projeto import Projeto
from Domain.Interfaces.IProjetoRepository import IProjetoRepository
from Infraestrcuture.databases.projeto_model import ProjetoModel


class projetoRepository(IProjetoRepository):
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

    def obter_projeto_por_id(self, projeto_id: int) -> Projeto | None:
        projeto_model = self.session.query(ProjetoModel).filter_by(id=projeto_id).first()
        if projeto_model is None:
            return None
        return Projeto(
            id=projeto_model.id,
            nome=projeto_model.nome,
            descricao=projeto_model.descricao
        )