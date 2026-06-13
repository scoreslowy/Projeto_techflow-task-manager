"""Rotas responsáveis pelo gerenciamento de tarefas."""

from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from .db import get_db

bp = Blueprint("tasks", __name__)

STATUS_LABELS = {
    "todo": "A Fazer",
    "doing": "Em Progresso",
    "done": "Concluído",
}

PRIORITY_LABELS = {
    "low": "Baixa",
    "medium": "Média",
    "high": "Alta",
}


def get_task(task_id: int):
    """Busca uma tarefa ou interrompe a requisição com erro 404."""
    task = get_db().execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        abort(404, description="Tarefa não encontrada.")
    return task


def validate_task(title: str, status: str, priority: str, due_date: str) -> list[str]:
    """Valida os campos obrigatórios de uma tarefa."""
    errors: list[str] = []
    if len(title.strip()) < 3:
        errors.append("O título deve possuir pelo menos 3 caracteres.")
    if len(title.strip()) > 120:
        errors.append("O título deve possuir no máximo 120 caracteres.")
    if status not in STATUS_LABELS:
        errors.append("O status informado é inválido.")
    if priority not in PRIORITY_LABELS:
        errors.append("A prioridade informada é inválida.")
    if due_date:
        try:
            date.fromisoformat(due_date)
        except ValueError:
            errors.append("A data limite é inválida.")
    return errors


@bp.get("/")
def index():
    """Exibe as tarefas agrupadas em um quadro Kanban."""
    database = get_db()
    query = request.args.get("q", "").strip()
    priority_filter = request.args.get("priority", "")
    status_filter = request.args.get("status", "")

    sql = "SELECT * FROM tasks WHERE 1 = 1"
    params: list[str] = []
    if query:
        sql += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])
    if priority_filter in PRIORITY_LABELS:
        sql += " AND priority = ?"
        params.append(priority_filter)
    if status_filter in STATUS_LABELS:
        sql += " AND status = ?"
        params.append(status_filter)
    sql += (
        " ORDER BY CASE priority WHEN 'high' THEN 1 "
        "WHEN 'medium' THEN 2 ELSE 3 END, due_date, id DESC"
    )

    tasks = database.execute(sql, params).fetchall()
    grouped = {
        status: [task for task in tasks if task["status"] == status]
        for status in STATUS_LABELS
    }
    return render_template(
        "index.html",
        grouped=grouped,
        status_labels=STATUS_LABELS,
        priority_labels=PRIORITY_LABELS,
        total=len(tasks),
        today=date.today().isoformat(),
        filters={"q": query, "priority": priority_filter, "status": status_filter},
    )


@bp.route("/tasks/new", methods=("GET", "POST"))
def create():
    """Cadastra uma nova tarefa."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "todo")
        priority = request.form.get("priority", "medium")
        due_date = request.form.get("due_date", "")
        errors = validate_task(title, status, priority, due_date)

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            database = get_db()
            database.execute(
                """
                INSERT INTO tasks (title, description, status, priority, due_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title, description, status, priority, due_date or None),
            )
            database.commit()
            flash("Tarefa criada com sucesso.", "success")
            return redirect(url_for("tasks.index"))

    return render_template(
        "form.html",
        page_title="Nova tarefa",
        status_labels=STATUS_LABELS,
        priority_labels=PRIORITY_LABELS,
        task=None,
    )


@bp.route("/tasks/<int:task_id>/edit", methods=("GET", "POST"))
def update(task_id: int):
    """Atualiza os dados de uma tarefa existente."""
    task = get_task(task_id)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "todo")
        priority = request.form.get("priority", "medium")
        due_date = request.form.get("due_date", "")
        errors = validate_task(title, status, priority, due_date)

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            database = get_db()
            database.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, status = ?, priority = ?, due_date = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (title, description, status, priority, due_date or None, task_id),
            )
            database.commit()
            flash("Tarefa atualizada com sucesso.", "success")
            return redirect(url_for("tasks.index"))

    return render_template(
        "form.html",
        page_title="Editar tarefa",
        status_labels=STATUS_LABELS,
        priority_labels=PRIORITY_LABELS,
        task=task,
    )


@bp.post("/tasks/<int:task_id>/delete")
def delete(task_id: int):
    """Exclui uma tarefa após confirmação na interface."""
    get_task(task_id)
    database = get_db()
    database.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    database.commit()
    flash("Tarefa excluída com sucesso.", "success")
    return redirect(url_for("tasks.index"))
