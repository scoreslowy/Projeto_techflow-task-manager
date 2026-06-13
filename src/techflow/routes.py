"""Rotas responsáveis pelo gerenciamento de tarefas."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .db import get_db

bp = Blueprint("tasks", __name__)

STATUS_LABELS = {
    "todo": "A Fazer",
    "doing": "Em Progresso",
    "done": "Concluído",
}


def validate_task(title: str, status: str) -> list[str]:
    """Valida os campos obrigatórios de uma tarefa."""
    errors: list[str] = []
    if len(title.strip()) < 3:
        errors.append("O título deve possuir pelo menos 3 caracteres.")
    if len(title.strip()) > 120:
        errors.append("O título deve possuir no máximo 120 caracteres.")
    if status not in STATUS_LABELS:
        errors.append("O status informado é inválido.")
    return errors


@bp.get("/")
def index():
    """Exibe as tarefas agrupadas em um quadro Kanban."""
    database = get_db()
    tasks = database.execute(
        "SELECT * FROM tasks ORDER BY created_at DESC, id DESC"
    ).fetchall()
    grouped = {
        status: [task for task in tasks if task["status"] == status]
        for status in STATUS_LABELS
    }
    return render_template(
        "index.html",
        grouped=grouped,
        status_labels=STATUS_LABELS,
        total=len(tasks),
    )


@bp.route("/tasks/new", methods=("GET", "POST"))
def create():
    """Cadastra uma nova tarefa."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "todo")
        errors = validate_task(title, status)

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            database = get_db()
            database.execute(
                "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
                (title, description, status),
            )
            database.commit()
            flash("Tarefa criada com sucesso.", "success")
            return redirect(url_for("tasks.index"))

    return render_template(
        "form.html",
        page_title="Nova tarefa",
        status_labels=STATUS_LABELS,
        task=None,
    )
