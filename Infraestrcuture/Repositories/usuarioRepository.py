from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from Domain.Entities.usuario import Usuario
from Infraestrcuture.databases.base import Base
from Infraestrcuture.databases.usuario_model import UsuarioModel

class UsuarioRepository:
    def __init__(self, session):
        self.session = session

    def adicionar_usuario(self, usuario: Usuario):
        usuario_model = UsuarioModel(
            nome=usuario.nome,
            email=usuario.email,
            senha=usuario.senha,
            ativo=usuario.ativo
        )
        self.session.add(usuario_model)
        self.session.commit()
        return usuario_model.id

    def obter_usuario_por_email(self, email: str):
        usuario_model = self.session.query(UsuarioModel).filter_by(email=email).first()
        if usuario_model:
            return Usuario(
                id=usuario_model.id,
                nome=usuario_model.nome,
                email=usuario_model.email,
                senha=usuario_model.senha,
                ativo=usuario_model.ativo
            )
        return None