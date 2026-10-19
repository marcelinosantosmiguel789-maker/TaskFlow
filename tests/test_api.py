from fastapi.testclient import TestClient

from FastAPI.main import create_app
from Infraestrcuture.databases.connection import DatabaseConnection


class TestApi:
    def setup_method(self):
        self.database = DatabaseConnection("sqlite:///:memory:")
        self.client = TestClient(create_app(self.database))
        self.client.__enter__()

    def teardown_method(self):
        self.client.__exit__(None, None, None)

    def test_startup_creates_schema_and_openapi_lists_routes(self):
        response = self.client.get("/projetos")

        assert response.status_code == 200
        assert response.json() == []
        assert self.client.get("/docs").status_code == 200
        openapi = self.client.get("/openapi.json").json()
        assert "/projetos" in openapi["paths"]
        assert "/tarefas/{tarefa_id}" in openapi["paths"]
        assert "/usuarios" in openapi["paths"]

    def test_cors_allows_dashboard_and_denies_other_origins(self):
        dashboard_origin = "https://taskflow-ews9keby.manus.space"
        preflight = self.client.options(
            "/projetos",
            headers={
                "Origin": dashboard_origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        assert preflight.status_code == 200
        assert preflight.headers["access-control-allow-origin"] == dashboard_origin

        response = self.client.get(
            "/projetos",
            headers={"Origin": "https://another-site.example"},
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" not in response.headers

    def test_project_and_task_lifecycle_and_relations(self):
        project_response = self.client.post(
            "/projetos",
            json={"nome": "Projeto", "descricao": "Descrição"},
        )
        assert project_response.status_code == 201
        project = project_response.json()
        assert self.client.get("/projetos").json() == [project]

        task_response = self.client.post(
            "/tarefas",
            json={"titulo": "Tarefa", "projeto_id": project["id"]},
        )
        assert task_response.status_code == 201
        task = task_response.json()
        assert task["projeto_id"] == project["id"]
        assert task["concluida"] is False
        assert self.client.get(f"/tarefas/{task['id']}").json() == task

        updated_task = self.client.patch(
            f"/tarefas/{task['id']}",
            json={"concluida": True, "titulo": "Tarefa concluída"},
        )
        assert updated_task.status_code == 200
        assert updated_task.json()["concluida"] is True
        assert updated_task.json()["titulo"] == "Tarefa concluída"

        listed_tasks = self.client.get(
            "/tarefas",
            params={"projeto_id": project["id"]},
        )
        assert listed_tasks.status_code == 200
        assert [item["id"] for item in listed_tasks.json()] == [task["id"]]

        updated_project = self.client.patch(
            f"/projetos/{project['id']}",
            json={"nome": "Projeto atualizado"},
        )
        assert updated_project.status_code == 200
        assert updated_project.json()["nome"] == "Projeto atualizado"
        assert self.client.delete(
            f"/projetos/{project['id']}"
        ).status_code == 409

        assert self.client.delete(f"/tarefas/{task['id']}").status_code == 204
        assert self.client.delete(
            f"/projetos/{project['id']}"
        ).status_code == 204
        assert self.client.get(f"/tarefas/{task['id']}").status_code == 404

    def test_missing_project_and_invalid_fields_have_http_errors(self):
        missing_project_task = self.client.post(
            "/tarefas",
            json={"titulo": "Tarefa", "projeto_id": 999},
        )
        assert missing_project_task.status_code == 404

        invalid_task = self.client.post(
            "/tarefas",
            json={"titulo": "   ", "projeto_id": 1},
        )
        assert invalid_task.status_code == 422

        assert self.client.get("/projetos/0").status_code == 422
        assert self.client.get(
            "/tarefas",
            params={"projeto_id": 999},
        ).status_code == 404

    def test_user_email_validation_duplicates_and_response_do_not_leak_password(self):
        invalid_email = self.client.post(
            "/usuarios",
            json={
                "nome": "Nome",
                "email": "not-an-email",
                "senha": "segredo",
            },
        )
        assert invalid_email.status_code == 422

        payload = {
            "nome": "Nome",
            "email": "NOME@example.com",
            "senha": "segredo",
        }
        created_user = self.client.post("/usuarios", json=payload)
        assert created_user.status_code == 201
        assert "senha" not in created_user.json()
        assert "segredo" not in created_user.text
        fetched_user = self.client.get(
            f"/usuarios/{created_user.json()['email']}"
        )
        assert fetched_user.status_code == 200
        assert fetched_user.json() == created_user.json()

        duplicate = self.client.post(
            "/usuarios",
            json={**payload, "email": "nome@example.com"},
        )
        assert duplicate.status_code == 409
