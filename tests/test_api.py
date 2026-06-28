from io import BytesIO


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["offline_first"] is True
    assert data["cpu_only"] is True


def test_upload_process_and_export_text(client):
    payload = b"Urgent Contract with Ada Lovelace about offline document intelligence."
    upload = client.post(
        "/upload",
        files={"file": ("sample.txt", BytesIO(payload), "text/plain")},
    )
    assert upload.status_code == 200
    document_id = upload.json()["id"]

    processed = client.post(f"/process?id={document_id}")
    assert processed.status_code == 200
    data = processed.json()
    assert data["filename"] == "sample.txt"
    assert data["priority"] == "high"
    assert "Ada Lovelace" in data["entities"]

    documents = client.get("/documents")
    assert documents.status_code == 200
    assert len(documents.json()) == 1

    exported = client.get("/export/json")
    assert exported.status_code == 200
    assert "sample.txt" in exported.text
