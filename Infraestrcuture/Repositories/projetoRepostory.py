from Domain.Exceptions import ProjetoComTarefasError
from Domain.Entities.projeto import Projeto
from Domain.Interfaces.IProjetoRepository import IProjetoRepository
from Infraestrcuture.databases.projeto_model import ProjetoModel
from Infraestrcuture.databases.tarefa_model import TarefaModel
from sqlalchemy.exc import IntegrityError


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
        return self._para_entidade(projeto_model)

    def atualizar_projeto(self, projeto_id: int, dados: dict):
        projeto_model = self.session.query(ProjetoModel).filter_by(
            id=projeto_id
        ).first()
        if projeto_model is None:
            return None
        for campo, valor in dados.items():
            setattr(projeto_model, campo, valor)
        self.session.commit()
        return self._para_entidade(projeto_model)

    def excluir_projeto(self, projeto_id: int) -> bool:
        projeto_model = self.session.query(ProjetoModel).filter_by(
            id=projeto_id
        ).first()
        if projeto_model is None:
            return False
        tem_tarefas = self.session.query(TarefaModel.id).filter_by(
            projeto_id=projeto_id
        ).first()
        if tem_tarefas is not None:
            raise ProjetoComTarefasError(
                "Não é possível excluir um projeto que possui tarefas."
            )
        self.session.delete(projeto_model)
        try:
            self.session.commit()
        except IntegrityError as error:
            self.session.rollback()
            raise ProjetoComTarefasError(
                "Não é possível excluir um projeto que possui tarefas."
            ) from error
        return True

    @staticmethod
    def _para_entidade(projeto_model: ProjetoModel) -> Projeto:
        return Projeto(
            id=projeto_model.id,
            nome=projeto_model.nome,
            descricao=projeto_model.descricao,
        )