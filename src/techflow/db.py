"""Acesso ao banco de dados SQLite."""

import sqlite3

import click
from flask import current_app, g


SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'todo',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (length(trim(title)) BETWEEN 3 AND 120),
    CHECK (status IN ('todo', 'doing', 'done'))
);
"""


def get_db() -> sqlite3.Connection:
    """Retorna uma conexão por contexto de requisição."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error: BaseException | None = None) -> None:
    """Fecha a conexão aberta no contexto atual."""
    database = g.pop("db", None)
    if database is not None:
        database.close()


def init_db() -> None:
    """Cria as tabelas necessárias quando ainda não existem."""
    database = get_db()
    database.executescript(SCHEMA)
    database.commit()


@click.command("init-db")
def init_db_command() -> None:
    """Recria a estrutura básica do banco via linha de comando."""
    init_db()
    click.echo("Banco de dados inicializado.")



@click.command("seed-demo")
def seed_demo_command() -> None:
    """Insere tarefas de demonstração sem duplicar dados existentes."""
    database = get_db()
    count = database.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count:
        click.echo("O banco já possui tarefas; nenhuma demonstração foi inserida.")
        return

    tasks = [
        ("Mapear fluxo da operação", "Levantar etapas da rotina logística.", "done"),
        ("Criar protótipo do Kanban", "Validar a visualização com os stakeholders.", "done"),
        ("Implementar cadastro de tarefas", "Disponibilizar formulário com validações.", "doing"),
        ("Configurar testes automatizados", "Cobrir regras de negócio e rotas principais.", "todo"),
        ("Preparar demonstração", "Organizar roteiro do vídeo pitch.", "todo"),
    ]
    database.executemany(
        "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)", tasks
    )
    database.commit()
    click.echo("Dados de demonstração inseridos.")


def init_app(app) -> None:
    """Registra os recursos de banco na aplicação."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_demo_command)
