import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Application.DTOs.tarefa_dto import mapear_tarefa_para_dto
from Application.UseCases.Projeto.BuscarProjeto import BuscarProjeto
from Application.UseCases.Projeto.CriarProjeto import criarProjeto
from Application.UseCases.Projeto.ListarProjetos import listarProjetos
from Application.UseCases.Tarefa.ObterTarefa import ObterTarefa
from Application.UseCases.Usuario.CriarUsuario import CriarUsuario
from Domain.Entities.projeto import Projeto
from Domain.Entities.tarefa import Tarefa
from Domain.Entities.usuario import Usuario
from Domain.Exceptions import ProjetoNaoEncontradoError
from Domain.Services.password_hasher import hash_password
from Infraestrcuture.Repositories.projetoRepostory import projetoRepository
from Infraestrcuture.Repositories.tarefaRepository import TarefaRepository
from Infraestrcuture.Repositories.usuarioRepository import UsuarioRepository
from Infraestrcuture.databases.base import Base
from Infraestrcuture.databases.projeto_model import ProjetoModel
from Infraestrcuture.databases.tarefa_model import TarefaModel


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
        self.assertEqual(
            projeto.id,
            mapear_tarefa_para_dto(tarefas[0]).projeto_id,
        )

    def test_tarefa_rejeita_projeto_inexistente(self):
        repository = TarefaRepository(self.session)
        tarefa = Tarefa(
            id=None,
            titulo="Tarefa",
            descricao=None,
            concluida=False,
            projeto_id=999,
        )

        with self.assertRaises(ProjetoNaoEncontradoError):
            repository.adicionar_tarefa(tarefa)

        self.assertEqual(self.session.query(TarefaModel).count(), 0)

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

        CriarUsuario(repository).criar_usuario(
            "Nome",
            "nome@example.com",
            "senha",
        )

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
        usuario_recuperado = repository.obter_usuario_por_email(
            usuario.email
        )

        self.assertIsNotNone(usuario_recuperado)
        self.assertFalse(usuario_recuperado.ativo)
        self.assertEqual(usuario.email, usuario_recuperado.email)
        self.assertTrue(usuario_recuperado.validar_senha("senha"))

    def test_email_duplicado_e_case_insensitive(self):
        repository = UsuarioRepository(self.session)
        usuario = Usuario(
            id=None,
            nome="Nome",
            email="nome@example.com",
            senha=hash_password("senha"),
        )
        repository.adicionar_usuario(usuario)

        with self.assertRaises(ValueError):
            repository.adicionar_usuario(
                Usuario(
                    id=None,
                    nome="Outro",
                    email="NOME@example.com",
                    senha=hash_password("senha"),
                )
            )

    def test_projeto_com_tarefas_nao_pode_ser_excluido(self):
        repository = projetoRepository(self.session)
        projeto_id = repository.adicionar_projeto(
            Projeto(id=None, nome="Projeto", descricao=None)
        )
        TarefaRepository(self.session).adicionar_tarefa(
            Tarefa(
                id=None,
                titulo="Tarefa",
                descricao=None,
                concluida=False,
                projeto_id=projeto_id,
            )
        )

        with self.assertRaises(ValueError):
            repository.excluir_projeto(projeto_id)

    def test_obter_tarefas_por_projeto(self):
        class FakeTarefaRepository:
            def obter_tarefas_por_projeto(self, projeto_id: int):
                if projeto_id == 1:
                    return [
                        Tarefa(
                            id=1,
                            titulo="Estudar Python",
                            descricao="Estudar Clean Architecture",
                            concluida=False,
                            projeto_id=1,
                        )
                    ]
                return []

        caso_de_uso = ObterTarefa(FakeTarefaRepository())

        tarefas = caso_de_uso.obter_por_projeto(1)

        self.assertEqual(len(tarefas), 1)
        self.assertEqual(tarefas[0].titulo, "Estudar Python")
        self.assertEqual(tarefas[0].projeto_id, 1)

    def test_obter_tarefas_por_projeto_sem_resultados(self):
        class FakeTarefaRepository:
            def obter_tarefas_por_projeto(self, projeto_id: int):
                return []

        caso_de_uso = ObterTarefa(FakeTarefaRepository())

        tarefas = caso_de_uso.obter_por_projeto(999)

        self.assertEqual(tarefas, [])
    def test_listar_projeto(self):
        class FakeProjetoRepository:
            def listar_projetos(self):
                return [
                    Projeto(
                        id=1,
                        nome="Projeto 1",
                        descricao="Descricao do Projeto 1"
                    ),
                    Projeto(
                        id=2,
                        nome="Projeto 2",
                        descricao="Descricao do Projeto 2"
                    )
                ]

        projetos = listarProjetos(FakeProjetoRepository()).listar()

        self.assertEqual(len(projetos), 2)
        self.assertEqual(
            [projeto.nome for projeto in projetos],
            ["Projeto 1", "Projeto 2"],
        )


if __name__ == "__main__":
    unittest.main()