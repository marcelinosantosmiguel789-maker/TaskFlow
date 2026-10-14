import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Application.DTOs.tarefa_dto import mapear_tarefa_para_dto
from Application.UseCases.Projeto.BuscarProjeto import BuscarProjeto
from Application.UseCases.Projeto.CriarProjeto import criarProjeto
from Application.UseCases.Usuario.CriarUsuario import CriarUsuario
from Domain.Entities.tarefa import Tarefa
from Domain.Entities.usuario import Usuario
from Domain.Services.password_hasher import hash_password
from Infraestrcuture.Repositories.projetoRepostory import projetoRepository
from Infraestrcuture.Repositories.tarefaRepository import TarefaRepository
from Infraestrcuture.Repositories.usuarioRepository import UsuarioRepository
from Infraestrcuture.databases.base import Base
from Infraestrcuture.databases.projeto_model import ProjetoModel


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_tarefa_round_trips_concluida_and_projeto(self):
        projeto = ProjetoModel(nome="Projeto", descricao="Descricao")
        self.session.add(projeto)
        self.session.commit()
        repository = TarefaRepository(self.session)
        tarefa = Tarefa(
            id=None,
            titulo="Tarefa",
            descricao="Descricao",
            concluida=True,
            projeto_id=projeto.id,
        )

        tarefa_id = repository.adicionar_tarefa(tarefa)
        tarefas = repository.obter_tarefas_por_projeto(projeto.id)

        self.assertEqual(tarefa_id, tarefas[0].id)
        self.assertTrue(tarefas[0].concluida)
        self.assertEqual(projeto.id, tarefas[0].projeto_id)
        self.assertTrue(mapear_tarefa_para_dto(tarefas[0]).concluida)

    def test_projeto_create_and_lookup_use_repository_contract(self):
        repository = projetoRepository(self.session)
        criar_projeto = criarProjeto(repository)

        projeto_id = criar_projeto.criar("Projeto", "Descricao")
        projeto = BuscarProjeto(repository).buscar_por_id(projeto_id)

        self.assertIsNotNone(projeto)
        self.assertEqual(projeto_id, projeto.id)
        self.assertEqual("Projeto", projeto.nome)
        self.assertIsNone(BuscarProjeto(repository).buscar_por_id(-1))

    def test_criar_usuario_persists_a_hash_that_can_be_verified(self):
        class CapturingRepository:
            def adicionar_usuario(self, usuario):
                self.usuario = usuario
                return 1

        repository = CapturingRepository()
        CriarUsuario(repository).criar_usuario("Nome", "nome@example.com", "senha")

        self.assertNotEqual("senha", repository.usuario.senha)
        self.assertTrue(repository.usuario.validar_senha("senha"))
        self.assertFalse(repository.usuario.validar_senha("incorreta"))

    def test_usuario_round_trips_ativo(self):
        repository = UsuarioRepository(self.session)
        usuario = Usuario(
            id=None,
            nome="Nome",
            email="nome@example.com",
            senha=hash_password("senha"),
            ativo=False,
        )

        repository.adicionar_usuario(usuario)
        usuario_recuperado = repository.obter_usuario_por_email(usuario.email)

        self.assertIsNotNone(usuario_recuperado)
        self.assertFalse(usuario_recuperado.ativo)
        self.assertEqual(usuario.email, usuario_recuperado.email)
        self.assertTrue(usuario_recuperado.validar_senha("senha"))

    def listar_projeto(self):
        repository = projetoRepository(self.session)
        criar_projeto = criarProjeto(repository)

        criar_projeto.criar("Projeto 1", "Descricao 1")
        criar_projeto.criar("Projeto 2", "Descricao 2")

        projetos = repository.listar_projetos()

        self.assertEqual(len(projetos), 2)
        self.assertEqual(projetos[0].nome, "Projeto 1")
        self.assertEqual(projetos[1].nome, "Projeto 2")


if __name__ == "__main__":
    unittest.main()
