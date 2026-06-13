import requests

BASE_URL = "http://localhost:5000"


def test_health_endpoint():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "model_version" in data


def test_predict_returns_label_and_confidence():
    r = requests.post(f"{BASE_URL}/predict", json={"text": "This is a great day"})
    assert r.status_code == 200
    data = r.json()
    assert data["label"] in ["POSITIVE", "NEGATIVE"]
    assert 0 <= data["confidence"] <= 1
    assert "model_version" in data


def test_predict_negative_text():
    r = requests.post(f"{BASE_URL}/predict", json={"text": "This is terrible and awful"})
    assert r.status_code == 200


def test_health_returns_model_version_unstable():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    assert r.json()["model_version"] == "unstable-v1"