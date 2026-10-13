from pydantic import BaseModel
from Domain.Entities.usuario import Usuario

class UsuarioDTO(BaseModel):
    id: int
    nome: str
    email: str

def mapear_usuario_para_dto(usuario: Usuario) -> UsuarioDTO:
    return UsuarioDTO(
        id=usuario.id,
        nome=usuario.nome,
        email=usuario.email
    )