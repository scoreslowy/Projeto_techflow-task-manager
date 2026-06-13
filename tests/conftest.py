"""Configurações compartilhadas dos testes."""

from pathlib import Path

import pytest

from techflow import create_app
from techflow.db import get_db


@pytest.fixture()
def app(tmp_path: Path):
    database_path = tmp_path / "test.sqlite3"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test",
            "DATABASE": str(database_path),
        }
    )

    with app.app_context():
        database = get_db()
        database.execute(
            "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
            ("Tarefa inicial", "Criada para os testes", "todo"),
        )
        database.commit()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
