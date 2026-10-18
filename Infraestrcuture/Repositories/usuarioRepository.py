from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from Domain.Exceptions import EmailDuplicadoError
from Domain.Entities.usuario import Usuario
from Domain.Interfaces.IUsuarioRepository import IUsuarioRepository
from Infraestrcuture.databases.usuario_model import UsuarioModel


class UsuarioRepository(IUsuarioRepository):
    def __init__(self, session):
        self.session = session

    def adicionar_usuario(self, usuario: Usuario):
        email = usuario.email.strip().lower()
        if self.session.query(UsuarioModel.id).filter(
            func.lower(UsuarioModel.email) == email
        ).first():
            raise EmailDuplicadoError("Já existe um usuário com este e-mail.")
        usuario_model = UsuarioModel(
            nome=usuario.nome,
            email=email,
            senha=usuario.senha,
            ativo=usuario.ativo
        )
        self.session.add(usuario_model)
        try:
            self.session.commit()
        except IntegrityError as error:
            self.session.rollback()
            raise EmailDuplicadoError(
                "Já existe um usuário com este e-mail."
            ) from error
        return usuario_model.id

    def obter_usuario_por_email(self, email: str):
        usuario_model = self.session.query(UsuarioModel).filter(
            func.lower(UsuarioModel.email) == email.strip().lower()
        ).first()
        if usuario_model:
            return Usuario(
                id=usuario_model.id,
                nome=usuario_model.nome,
                email=usuario_model.email,
                senha=usuario_model.senha,
                ativo=usuario_model.ativo
            )
        return None