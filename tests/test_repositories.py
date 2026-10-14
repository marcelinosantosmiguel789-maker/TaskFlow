import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Application.DTOs.tarefa_dto import mapear_tarefa_para_dto
from Domain.Entities.tarefa import Tarefa
from Domain.Entities.usuario import Usuario
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

    def test_usuario_round_trips_ativo(self):
        repository = UsuarioRepository(self.session)
        usuario = Usuario(
            id=None,
            nome="Nome",
            email="nome@example.com",
            senha="senha",
            ativo=False,
        )

        repository.adicionar_usuario(usuario)
        usuario_recuperado = repository.obter_usuario_por_email(usuario.email)

        self.assertIsNotNone(usuario_recuperado)
        self.assertFalse(usuario_recuperado.ativo)
        self.assertEqual(usuario.email, usuario_recuperado.email)


if __name__ == "__main__":
    unittest.main()
