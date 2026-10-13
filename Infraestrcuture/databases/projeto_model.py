
from sqlalchemy import Column, Integer, String

from Infraestrcuture.databases.base import Base


class ProjetoModel(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=True)
