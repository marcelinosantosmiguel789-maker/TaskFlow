from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from Domain.Entities.projeto import Projeto
from Infraestrcuture.databases.base import Base
from Infraestrcuture.databases.projeto_model import ProjetoModel

class projetoRepository:
    def __init__(self, session):
        self.session = session
    def adicionarProjeto(self, projeto: Projeto):
        Projeto_Model = ProjetoModel(
            nome=projeto.nome,
            descricao=projeto.descricao,
            data_inicio=projeto.data_inicio,
            data_fim=projeto.data_fim
        )
        self.session.add(Projeto_Model)
        self.session.commit()
        return Projeto_Model.id
    
