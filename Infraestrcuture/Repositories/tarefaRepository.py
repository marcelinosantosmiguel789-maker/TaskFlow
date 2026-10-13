from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from Infraestrcuture.databases.base import Base
from Domain.Entities.tarefa import Tarefa
from Infraestrcuture.databases.tarefa_model import TarefaModel

class TarefaRepository:
    def __init__(self, session):
        self.session = session

    def adicionar_tarefa(self, tarefa: Tarefa):
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
        return [Tarefa(
            id=tarefa.id,
            titulo=tarefa.titulo,
            descricao=tarefa.descricao,
            concluida=tarefa.concluida,
            projeto_id=tarefa.projeto_id
        ) for tarefa in tarefas_model]