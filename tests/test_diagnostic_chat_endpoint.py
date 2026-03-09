from api.vetdict_api import app


def test_chat_returns_species_guidance_for_cat():
    client = app.test_client()
    resp = client.post(
        "/api/diagnostic-chat/chat",
        json={"species": "cat", "message": "猫が咳と呼吸困難です"},
    )
    assert resp.status_code == 200
    payload = resp.get_json()
    assert payload["species"] == "cat"
    assert "species_guidance" in payload
    assert "猫として解析" in payload["species_guidance"]
    assert payload["response"].startswith(payload["species_guidance"])


def test_chat_species_guidance_differs_by_species():
    client = app.test_client()
    cat_resp = client.post(
        "/api/diagnostic-chat/chat",
        json={"species": "cat", "message": "猫が咳をしています"},
    )
    dog_resp = client.post(
        "/api/diagnostic-chat/chat",
        json={"species": "dog", "message": "犬が咳をしています"},
    )
    assert cat_resp.status_code == 200
    assert dog_resp.status_code == 200
    cat_payload = cat_resp.get_json()
    dog_payload = dog_resp.get_json()
    assert cat_payload["species_guidance"] != dog_payload["species_guidance"]
    assert "猫" in cat_payload["species_guidance"]
    assert "犬" in dog_payload["species_guidance"]

