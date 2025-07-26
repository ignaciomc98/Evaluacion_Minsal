# app/tests/test_register.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user_duplicate_email():
    payload = {
        "name": "Duplicado",
        "email": "duplicado@correo.co",
        "password": "Hunter22",
        "phones": []
    }

    client.post("/register", json=payload)
    response = client.post("/register", json=payload)

    assert response.status_code == 400
    assert response.json() == {"mensaje": "El correo ya está registrado"}
