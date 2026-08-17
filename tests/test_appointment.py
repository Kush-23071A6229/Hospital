def create_patient(client):
    response = client.post(
        "/patients",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
        },
    )

    assert response.status_code == 201
    return response.json()["id"]


def create_doctor(client):
    response = client.post(
        "/doctors",
        json={
            "name": "Dr. Smith",
            "specialization": "Cardiology",
        },
    )

    assert response.status_code == 201
    return response.json()["id"]


def create_appointment(client, patient_id, doctor_id, start, end):
    return client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": start,
            "appointment_end": end,
        },
    )


def test_create_appointment(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    response = create_appointment(
        client,
        patient_id,
        doctor_id,
        "2026-08-20T10:00:00",
        "2026-08-20T11:00:00",
    )

    assert response.status_code == 201

    data = response.json()

    assert data["patient_id"] == patient_id
    assert data["doctor_id"] == doctor_id


def test_overlapping_appointment_rejected(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    first = create_appointment(
        client,
        patient_id,
        doctor_id,
        "2026-08-20T10:00:00",
        "2026-08-20T11:00:00",
    )

    assert first.status_code == 201

    overlapping = create_appointment(
        client,
        patient_id,
        doctor_id,
        "2026-08-20T10:30:00",
        "2026-08-20T11:30:00",
    )

    assert overlapping.status_code == 409


def test_back_to_back_appointment_allowed(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    first = create_appointment(
        client,
        patient_id,
        doctor_id,
        "2026-08-20T10:00:00",
        "2026-08-20T11:00:00",
    )

    assert first.status_code == 201

    second = create_appointment(
        client,
        patient_id,
        doctor_id,
        "2026-08-20T11:00:00",
        "2026-08-20T12:00:00",
    )

    assert second.status_code == 201
