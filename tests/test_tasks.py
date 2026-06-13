"""Testes funcionais do CRUD de tarefas."""

from techflow.db import get_db


def test_index_displays_registered_task(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Tarefa inicial" in response.data
    assert b"Quadro de tarefas" in response.data


def test_create_task(client, app):
    response = client.post(
        "/tasks/new",
        data={
            "title": "Validar entrega",
            "description": "Conferir critérios da atividade",
            "status": "doing",
            "priority": "high",
            "due_date": "2026-06-20",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Tarefa criada com sucesso" in response.data
    with app.app_context():
        task = get_db().execute(
            "SELECT * FROM tasks WHERE title = ?", ("Validar entrega",)
        ).fetchone()
        assert task is not None
        assert task["status"] == "doing"
        assert task["priority"] == "high"
        assert task["due_date"] == "2026-06-20"


def test_rejects_short_title(client):
    response = client.post(
        "/tasks/new",
        data={
            "title": "Oi",
            "description": "Inválida",
            "status": "todo",
            "priority": "medium",
            "due_date": "",
        },
    )

    assert response.status_code == 200
    assert b"pelo menos 3 caracteres" in response.data


def test_update_task(client, app):
    response = client.post(
        "/tasks/1/edit",
        data={
            "title": "Tarefa atualizada",
            "description": "Descrição revisada",
            "status": "done",
            "priority": "low",
            "due_date": "2026-06-30",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Tarefa atualizada com sucesso" in response.data
    with app.app_context():
        task = get_db().execute("SELECT * FROM tasks WHERE id = 1").fetchone()
        assert task["title"] == "Tarefa atualizada"
        assert task["status"] == "done"


def test_delete_task(client, app):
    response = client.post("/tasks/1/delete", follow_redirects=True)

    assert response.status_code == 200
    assert b"Tarefa exclu" in response.data
    with app.app_context():
        task = get_db().execute("SELECT * FROM tasks WHERE id = 1").fetchone()
        assert task is None


def test_missing_task_returns_404(client):
    response = client.get("/tasks/999/edit")

    assert response.status_code == 404


def test_filter_by_priority(client, app):
    with app.app_context():
        database = get_db()
        database.execute(
            """
            INSERT INTO tasks (title, description, status, priority)
            VALUES (?, ?, ?, ?)
            """,
            ("Tarefa crítica", "Deve aparecer no filtro", "todo", "high"),
        )
        database.commit()

    response = client.get("/?priority=high")

    assert response.status_code == 200
    assert b"Tarefa cr" in response.data
    assert b"Tarefa inicial" not in response.data
