from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from Infraestrcuture.databases.base import Base

class tarefa_model(DatabaseConnection.base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=True)
    concluida = Column(Boolean, default=False)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=False)