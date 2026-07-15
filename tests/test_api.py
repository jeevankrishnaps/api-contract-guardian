from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_create_and_get_user():
    res=client.post("/v1/users",json={"username":"jeevan","email":"ax.com"})
    assert res.status_code==201
    user_id=res.json()["id"]
    res=client.get(f"/v1/users/{user_id}")
    assert res.status_code==200
    assert res.json()["username"]=="jeevan"


def test_get_missing_user():
    res=client.get("/v1/users/9999")
    assert res.status_code==404

def test_health():
    res=client.get("/health")
    assert res.status_code==200