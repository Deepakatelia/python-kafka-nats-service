# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.appointment_dto import AppointmentDto  # noqa: F401
from openapi_server.models.appointment_for_update_dto import AppointmentForUpdateDto  # noqa: F401
from openapi_server.models.appointment_paged_result_dto import AppointmentPagedResultDto  # noqa: F401
from openapi_server.models.appointments_delete_delete200_response import AppointmentsDeleteDelete200Response  # noqa: F401
from openapi_server.models.appointments_get_slots_get200_response import AppointmentsGetSlotsGet200Response  # noqa: F401
from openapi_server.models.message_dto import MessageDto  # noqa: F401


def test_appointments_create_post(client: TestClient):
    """Test case for appointments_create_post

    
    """
    appointment_dto = {"appointment_type":6,"patient_name":"patientName","patient_id":"patientId","appointment_status":1,"symptoms":"symptoms","patient_image":"patientImage","created_at":"createdAt","doctor_name":"doctorName","connecty_cube_id":"connectyCubeId","created_by":"createdBy","doctor_id":"doctorId","slot_time":"slotTime","slot_id":"slotId","id":"id","appointment_date":"2000-01-23","doctor_image":"doctorImage","is_exist":1,"updated_at":"updatedAt"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "POST",
        "/Appointments/create",
        headers=headers,
        json=appointment_dto,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_appointments_delete_delete(client: TestClient):
    """Test case for appointments_delete_delete

    
    """
    params = [("id", 'id_example')]
    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "DELETE",
        "/Appointments/delete",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_appointments_get_all_by_doc_id_and_patient_id_get(client: TestClient):
    """Test case for appointments_get_all_by_doc_id_and_patient_id_get

    
    """
    params = [("patient_id", 'patient_id_example'),     ("doctor_id", 'doctor_id_example')]
    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/Appointments/getAllByDocIdAndPatientId",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_appointments_get_all_by_doc_id_get(client: TestClient):
    """Test case for appointments_get_all_by_doc_id_get

    
    """
    params = [("doctor_id", 'doctor_id_example'),     ("date", '2013-10-20')]
    headers = {
    }
    response = client.request(
        "GET",
        "/Appointments/getAllByDocId",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_appointments_get_all_get(client: TestClient):
    """Test case for appointments_get_all_get

    
    """
    params = [("patient_id", 'patient_id_example'),     ("date", '2013-10-20'),     ("order", 'order_example'),     ("limit", 56)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/Appointments/getAll",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_appointments_get_get(client: TestClient):
    """Test case for appointments_get_get

    
    """
    params = [("id", 'id_example')]
    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/Appointments/get",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_appointments_get_patient_latest_appointments_get(client: TestClient):
    """Test case for appointments_get_patient_latest_appointments_get

    
    """
    params = [("patient_id", 'patient_id_example'),     ("date", '2013-10-20'),     ("time", 'time_example'),     ("limit", 3.4)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/Appointments/getPatientLatestAppointments",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_appointments_get_slots_get(client: TestClient):
    """Test case for appointments_get_slots_get

    
    """
    params = [("doctor_id", 'doctor_id_example'),     ("date", '2013-10-20')]
    headers = {
    }
    response = client.request(
        "GET",
        "/Appointments/getSlots",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_appointments_get_standard_slots_get(client: TestClient):
    """Test case for appointments_get_standard_slots_get

    
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "GET",
        "/Appointments/getStandardSlots",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_appointments_update_put(client: TestClient):
    """Test case for appointments_update_put

    
    """
    appointment_for_update_dto = {"appointment_type":0,"patient_name":"patientName","patient_id":"patientId","appointment_status":1,"symptoms":"symptoms","patient_image":"patientImage","created_at":"createdAt","doctor_name":"doctorName","connecty_cube_id":"connectyCubeId","created_by":"createdBy","doctor_id":"doctorId","slot_time":"slotTime","slot_id":"slotId","id":"id","appointment_date":"2000-01-23","doctor_image":"doctorImage","is_exist":1,"updated_at":"updatedAt"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    response = client.request(
        "PUT",
        "/Appointments/update",
        headers=headers,
        json=appointment_for_update_dto,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

