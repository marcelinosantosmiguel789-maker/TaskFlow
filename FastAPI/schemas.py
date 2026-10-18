from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


def _texto_obrigatorio(valor: str) -> str:
    valor = valor.strip()
    if not valor:
        raise ValueError("Este campo é obrigatório.")
    return valor


class ProjetoCriacao(BaseModel):
    nome: str = Field(min_length=1, max_length=255)
    descricao: str | None = Field(default=None, max_length=255)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        return _texto_obrigatorio(valor)


class ProjetoAtualizacao(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=255)
    descricao: str | None = Field(default=None, max_length=255)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str | None) -> str | None:
        return _texto_obrigatorio(valor) if valor is not None else None

    @model_validator(mode="after")
    def validar_campos_atualizados(self):
        if not self.model_fields_set:
            raise ValueError("Informe ao menos um campo para atualizar.")
        if "nome" in self.model_fields_set and self.nome is None:
            raise ValueError("O nome do projeto não pode ser nulo.")
        return self


class TarefaCriacao(BaseModel):
    titulo: str = Field(min_length=1, max_length=255)
    descricao: str | None = Field(default=None, max_length=255)
    projeto_id: int = Field(gt=0)

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, valor: str) -> str:
        return _texto_obrigatorio(valor)


class TarefaAtualizacao(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=255)
    descricao: str | None = Field(default=None, max_length=255)
    concluida: bool | None = None

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, valor: str | None) -> str | None:
        return _texto_obrigatorio(valor) if valor is not None else None

    @model_validator(mode="after")
    def validar_campos_atualizados(self):
        if not self.model_fields_set:
            raise ValueError("Informe ao menos um campo para atualizar.")
        if "titulo" in self.model_fields_set and self.titulo is None:
            raise ValueError("O título da tarefa não pode ser nulo.")
        if "concluida" in self.model_fields_set and self.concluida is None:
            raise ValueError("O status concluida deve ser verdadeiro ou falso.")
        return self


class UsuarioCriacao(BaseModel):
    nome: str = Field(min_length=1, max_length=255)
    email: EmailStr
    senha: str = Field(min_length=1, max_length=255)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        return _texto_obrigatorio(valor)

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("A senha é obrigatória.")
        return valor
