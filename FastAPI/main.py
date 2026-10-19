from contextlib import asynccontextmanager
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from sqlalchemy.orm import Session

from Application.DTOs.projeto_dto import ProjetoDTO, mapear_projeto_para_dto
from Application.DTOs.tarefa_dto import TarefaDTO, mapear_tarefa_para_dto
from Application.DTOs.usuario_dto import UsuarioDTO, mapear_usuario_para_dto
from Application.UseCases.Projeto.AtualizarProjeto import AtualizarProjeto
from Application.UseCases.Projeto.BuscarProjeto import BuscarProjeto
from Application.UseCases.Projeto.CriarProjeto import criarProjeto
from Application.UseCases.Projeto.ExcluirProjeto import ExcluirProjeto
from Application.UseCases.Projeto.ListarProjetos import listarProjetos
from Application.UseCases.Tarefa.AtualizarTarefa import AtualizarTarefa
from Application.UseCases.Tarefa.CriarTarefa import CriarTarefa
from Application.UseCases.Tarefa.ExcluirTarefa import ExcluirTarefa
from Application.UseCases.Usuario.CriarUsuario import CriarUsuario
from Application.UseCases.Usuario.UsuarioProEmail import (
    ObterUsuarioPorEmail,
)
from Domain.Exceptions import (
    DadosInvalidosError,
    EmailDuplicadoError,
    ProjetoComTarefasError,
    RecursoNaoEncontradoError,
)
from FastAPI.schemas import (
    ProjetoAtualizacao,
    ProjetoCriacao,
    TarefaAtualizacao,
    TarefaCriacao,
    UsuarioCriacao,
)
from Infraestrcuture.Repositories.projetoRepostory import projetoRepository
from Infraestrcuture.Repositories.tarefaRepository import TarefaRepository
from Infraestrcuture.Repositories.usuarioRepository import UsuarioRepository
from Infraestrcuture.databases.connection import DatabaseConnection


def get_session(request: Request) -> Generator[Session, None, None]:
    session = request.app.state.database.create_session()
    try:
        yield session
    finally:
        session.close()


def get_project_repository(
    session: Session = Depends(get_session),
) -> projetoRepository:
    return projetoRepository(session)


def get_task_repository(
    session: Session = Depends(get_session),
) -> TarefaRepository:
    return TarefaRepository(session)


def get_user_repository(
    session: Session = Depends(get_session),
) -> UsuarioRepository:
    return UsuarioRepository(session)


def create_app(database: DatabaseConnection | None = None) -> FastAPI:
    database = database or DatabaseConnection()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            if database.engine is None:
                database.establish_connection()
            if database.session_factory is None:
                database.configure_session_factory()
            database.generate_database_schema()
            app.state.database = database
            yield
        finally:
            if database.engine is not None:
                database.engine.dispose()
            database.engine = None
            database.session_factory = None

    app = FastAPI(
        title="TaskFlow API",
        description="API de gerenciamento de projetos, tarefas e usuários.",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://taskflow-ews9keby.manus.space"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(RecursoNaoEncontradoError)
    async def recurso_nao_encontrado_handler(_request, error):
        return JSONResponse(status_code=404, content={"detail": str(error)})

    @app.exception_handler(ProjetoComTarefasError)
    async def projeto_com_tarefas_handler(_request, error):
        return JSONResponse(status_code=409, content={"detail": str(error)})

    @app.exception_handler(EmailDuplicadoError)
    async def email_duplicado_handler(_request, error):
        return JSONResponse(status_code=409, content={"detail": str(error)})

    @app.exception_handler(DadosInvalidosError)
    async def validacao_handler(_request, error):
        return JSONResponse(status_code=422, content={"detail": str(error)})

    @app.get("/projetos", response_model=list[ProjetoDTO], tags=["projetos"])
    def listar_projetos(
        repository: projetoRepository = Depends(get_project_repository),
    ):
        projetos = listarProjetos(repository).listar()
        return [mapear_projeto_para_dto(projeto) for projeto in projetos]

    @app.post(
        "/projetos",
        response_model=ProjetoDTO,
        status_code=201,
        tags=["projetos"],
    )
    def criar_projeto(
        dados: ProjetoCriacao,
        repository: projetoRepository = Depends(get_project_repository),
    ):
        projeto_id = criarProjeto(repository).criar(
            dados.nome,
            dados.descricao,
        )
        projeto = BuscarProjeto(repository).buscar_por_id(projeto_id)
        return mapear_projeto_para_dto(projeto)

    @app.get(
        "/projetos/{projeto_id}",
        response_model=ProjetoDTO,
        tags=["projetos"],
    )
    def buscar_projeto(
        projeto_id: int = Path(gt=0),
        repository: projetoRepository = Depends(get_project_repository),
    ):
        projeto = BuscarProjeto(repository).buscar_por_id(projeto_id)
        if projeto is None:
            raise HTTPException(status_code=404, detail="Projeto não encontrado.")
        return mapear_projeto_para_dto(projeto)

    @app.patch(
        "/projetos/{projeto_id}",
        response_model=ProjetoDTO,
        tags=["projetos"],
    )
    def atualizar_projeto(
        dados: ProjetoAtualizacao,
        projeto_id: int = Path(gt=0),
        repository: projetoRepository = Depends(get_project_repository),
    ):
        projeto = AtualizarProjeto(repository).atualizar(
            projeto_id,
            dados.model_dump(exclude_unset=True),
        )
        if projeto is None:
            raise HTTPException(status_code=404, detail="Projeto não encontrado.")
        return mapear_projeto_para_dto(projeto)

    @app.delete(
        "/projetos/{projeto_id}",
        status_code=204,
        tags=["projetos"],
    )
    def excluir_projeto(
        projeto_id: int = Path(gt=0),
        repository: projetoRepository = Depends(get_project_repository),
    ):
        if not ExcluirProjeto(repository).excluir(projeto_id):
            raise HTTPException(status_code=404, detail="Projeto não encontrado.")
        return Response(status_code=204)

    @app.post(
        "/tarefas",
        response_model=TarefaDTO,
        status_code=201,
        tags=["tarefas"],
    )
    def criar_tarefa(
        dados: TarefaCriacao,
        repository: TarefaRepository = Depends(get_task_repository),
    ):
        tarefa_id = CriarTarefa(repository).criar(
            dados.titulo,
            dados.descricao,
            dados.projeto_id,
        )
        tarefa = repository.obter_tarefa_por_id(tarefa_id)
        return mapear_tarefa_para_dto(tarefa)

    @app.get("/tarefas", response_model=list[TarefaDTO], tags=["tarefas"])
    def listar_tarefas(
        projeto_id: int = Query(gt=0),
        repository: TarefaRepository = Depends(get_task_repository),
        project_repository: projetoRepository = Depends(
            get_project_repository
        ),
    ):
        if BuscarProjeto(project_repository).buscar_por_id(projeto_id) is None:
            raise HTTPException(status_code=404, detail="Projeto não encontrado.")
        tarefas = repository.obter_tarefas_por_projeto(projeto_id)
        return [mapear_tarefa_para_dto(tarefa) for tarefa in tarefas]

    @app.get(
        "/tarefas/{tarefa_id}",
        response_model=TarefaDTO,
        tags=["tarefas"],
    )
    def buscar_tarefa(
        tarefa_id: int = Path(gt=0),
        repository: TarefaRepository = Depends(get_task_repository),
    ):
        tarefa = repository.obter_tarefa_por_id(tarefa_id)
        if tarefa is None:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
        return mapear_tarefa_para_dto(tarefa)

    @app.patch(
        "/tarefas/{tarefa_id}",
        response_model=TarefaDTO,
        tags=["tarefas"],
    )
    def atualizar_tarefa(
        dados: TarefaAtualizacao,
        tarefa_id: int = Path(gt=0),
        repository: TarefaRepository = Depends(get_task_repository),
    ):
        tarefa = AtualizarTarefa(repository).atualizar(
            tarefa_id,
            dados.model_dump(exclude_unset=True),
        )
        if tarefa is None:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
        return mapear_tarefa_para_dto(tarefa)

    @app.delete(
        "/tarefas/{tarefa_id}",
        status_code=204,
        tags=["tarefas"],
    )
    def excluir_tarefa(
        tarefa_id: int = Path(gt=0),
        repository: TarefaRepository = Depends(get_task_repository),
    ):
        if not ExcluirTarefa(repository).excluir(tarefa_id):
            raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
        return Response(status_code=204)

    @app.post(
        "/usuarios",
        response_model=UsuarioDTO,
        status_code=201,
        tags=["usuarios"],
    )
    def criar_usuario(
        dados: UsuarioCriacao,
        repository: UsuarioRepository = Depends(get_user_repository),
    ):
        CriarUsuario(repository).criar_usuario(
            dados.nome,
            str(dados.email),
            dados.senha,
        )
        usuario = ObterUsuarioPorEmail(repository).obter_usuario_por_email(
            str(dados.email)
        )
        return mapear_usuario_para_dto(usuario)

    @app.get(
        "/usuarios/{email}",
        response_model=UsuarioDTO,
        tags=["usuarios"],
    )
    def buscar_usuario(
        email: EmailStr,
        repository: UsuarioRepository = Depends(get_user_repository),
    ):
        usuario = ObterUsuarioPorEmail(repository).obter_usuario_por_email(
            str(email)
        )
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        return mapear_usuario_para_dto(usuario)

    return app


app = create_app()
