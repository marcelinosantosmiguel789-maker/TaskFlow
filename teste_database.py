
from Infraestrcuture.databases.connection import DatabaseConnection
from Infraestrcuture.databases.projeto_model import ProjetoModel

db = DatabaseConnection()
db.establish_connection()
db.configure_session_factory()

sessao = db.create_session()

try:
    projeto = ProjetoModel(
        nome="TaskFlow",
        descricao="Projeto de estudo de arquitetura limpa e SQLAlchemy"
    )

    sessao.add(projeto)
    sessao.commit()
    sessao.refresh(projeto)

    print(f"Projeto criado com sucesso! ID: {projeto.id}")

except Exception:
    sessao.rollback()
    raise

finally:
    sessao.close()
