from Infraestrcuture.databases.connection import DatabaseConnection
from Infraestrcuture.Repositories.projetoRepostory import projetoRepository
from Domain.Entities.projeto import Projeto

db = DatabaseConnection()
db.establish_connection()
db.configure_session_factory()

sessao = db.create_session()

try:
    projeto_repo = projetoRepository(sessao)

    novo_projeto = Projeto(
        id=None,
        nome="TaskFlow",
        descricao="Projeto de estudo de arquitetura limpa e SQLAlchemy"
    )

    projeto_id = projeto_repo.adicionar_projeto(novo_projeto)

    print(f"Projeto criado com sucesso! ID: {projeto_id}")
except Exception:
    sessao.rollback()
    raise
finally:
    sessao.close()