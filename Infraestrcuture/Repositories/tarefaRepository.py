from Domain.Exceptions import ProjetoNaoEncontradoError
from Domain.Entities.tarefa import Tarefa
from Domain.Interfaces.ITarefaRepository import ITarefaRepository
from Infraestrcuture.databases.projeto_model import ProjetoModel
from Infraestrcuture.databases.tarefa_model import TarefaModel


class TarefaRepository(ITarefaRepository):
    def __init__(self, session):
        self.session = session

    def adicionar_tarefa(self, tarefa: Tarefa):
        projeto = self.session.query(ProjetoModel).filter_by(
            id=tarefa.projeto_id
        ).first()
        if projeto is None:
            raise ProjetoNaoEncontradoError(
                f"Projeto {tarefa.projeto_id} não encontrado."
            )
        tarefa_model = TarefaModel(
            titulo=tarefa.titulo,
            descricao=tarefa.descricao,
            concluida=tarefa.concluida,
            projeto_id=tarefa.projeto_id
        )
        self.session.add(tarefa_model)
        self.session.commit()
        return tarefa_model.id

    def obter_tarefas_por_projeto(self, projeto_id: int):
        tarefas_model = self.session.query(TarefaModel).filter_by(projeto_id=projeto_id).all()
        return [self._para_entidade(tarefa) for tarefa in tarefas_model]

    def obter_tarefa_por_id(self, tarefa_id: int) -> Tarefa | None:
        tarefa_model = self.session.query(TarefaModel).filter_by(
            id=tarefa_id
        ).first()
        if tarefa_model is None:
            return None
        return self._para_entidade(tarefa_model)

    def atualizar_tarefa(self, tarefa_id: int, dados: dict):
        tarefa_model = self.session.query(TarefaModel).filter_by(
            id=tarefa_id
        ).first()
        if tarefa_model is None:
            return None
        for campo, valor in dados.items():
            setattr(tarefa_model, campo, valor)
        self.session.commit()
        return self._para_entidade(tarefa_model)

    def excluir_tarefa(self, tarefa_id: int) -> bool:
        tarefa_model = self.session.query(TarefaModel).filter_by(
            id=tarefa_id
        ).first()
        if tarefa_model is None:
            return False
        self.session.delete(tarefa_model)
        self.session.commit()
        return True

    @staticmethod
    def _para_entidade(tarefa_model: TarefaModel) -> Tarefa:
        return Tarefa(
            id=tarefa_model.id,
            titulo=tarefa_model.titulo,
            descricao=tarefa_model.descricao,
            concluida=tarefa_model.concluida,
            projeto_id=tarefa_model.projeto_id,
        )