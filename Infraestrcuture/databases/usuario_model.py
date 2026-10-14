from sqlalchemy import Boolean, Column, Integer, String

from Infraestrcuture.databases.base import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
