"""Fábrica da aplicação TechFlow Task Manager."""

from pathlib import Path

from flask import Flask

from . import db


def create_app(test_config: dict | None = None) -> Flask:
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=str(Path(app.instance_path) / "techflow.sqlite3"),
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)

    from . import routes

    app.register_blueprint(routes.bp)

    with app.app_context():
        db.init_db()

    @app.get("/health")
    def health() -> dict[str, str]:
        """Endpoint simples para monitoramento da aplicação."""
        return {"status": "ok", "service": "techflow-task-manager"}

    return app
