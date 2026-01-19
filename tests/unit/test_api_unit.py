import runpy

import pytest

from app.api import app, _get_int


@pytest.fixture()
def client():
    app.testing = True
    return app.test_client()


def test_get_int_missing_param_raises(client):
    # Necesitamos un request context para que request.args exista
    with app.test_request_context("/sum"):
        with pytest.raises(ValueError):
            _get_int("a")


def test_sub_route_invalid_params_returns_400(client):
    # Fuerza el except de /sub (faltan params)
    r = client.get("/sub")  # sin ?a=...&b=...
    assert r.status_code == 400
    assert r.is_json
    assert "error" in r.get_json()


def test_run_as_main_covers_app_run(monkeypatch):
    import sys
    import runpy
    from flask.app import Flask

    def fake_run(self, *args, **kwargs):
        return None

    monkeypatch.setattr(Flask, "run", fake_run)

    # Quitar el módulo para evitar el RuntimeWarning en CI
    sys.modules.pop("app.api", None)

    runpy.run_module("app.api", run_name="__main__")


