
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from Infraestrcuture.databases.base import Base


class TarefaModel(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=True)
    concluida = Column(Boolean, default=False)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=False)
