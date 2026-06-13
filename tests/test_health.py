"""Testes do endpoint de monitoramento."""


def test_health_returns_service_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "service": "techflow-task-manager",
        "status": "ok",
    }
