def test_create_patient(client):
    response = client.post(
        "/patients",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["phone"] == "9876543210"


def test_get_patients(client):
    client.post(
        "/patients",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
        },
    )

    response = client.get("/patients")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "John Doe"


def test_get_patient_by_id(client):
    create_response = client.post(
        "/patients",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
        },
    )

    patient_id = create_response.json()["id"]

    response = client.get(
        f"/patients/{patient_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == patient_id
    assert data["name"] == "John Doe"


def test_get_missing_patient(client):
    response = client.get("/patients/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"


def test_duplicate_patient_email(client):
    patient = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "9876543210",
    }

    first_response = client.post(
        "/patients",
        json=patient,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/patients",
        json=patient,
    )

    assert second_response.status_code == 409
    assert (
        second_response.json()["detail"]
        == "Patient with this email already exists"
    )