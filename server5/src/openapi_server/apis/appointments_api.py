# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.appointment_dto import AppointmentDto
from openapi_server.models.appointment_for_update_dto import AppointmentForUpdateDto
from openapi_server.models.appointment_paged_result_dto import AppointmentPagedResultDto
from openapi_server.models.appointments_delete_delete200_response import AppointmentsDeleteDelete200Response
from openapi_server.models.appointments_get_slots_get200_response import AppointmentsGetSlotsGet200Response
from openapi_server.models.message_dto import MessageDto
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()


@router.post(
    "/Appointments/create",
    responses={
        201: {"model": AppointmentDto, "description": "Success"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
        422: {"model": MessageDto, "description": "Invalid Inputs"},
    },
    tags=["Appointments"],
    response_model_by_alias=True,
)
async def appointments_create_post(
    appointment_dto: AppointmentDto = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> AppointmentDto:
    ...


@router.delete(
    "/Appointments/delete",
    responses={
        200: {"model": AppointmentsDeleteDelete200Response, "description": "Success"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
        422: {"model": MessageDto, "description": "Invalid Inputs"},
    },
    tags=["Appointments"],
    response_model_by_alias=True,
)
async def appointments_delete_delete(
    id: str = Query(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> AppointmentsDeleteDelete200Response:
    ...


@router.get(
    "/Appointments/getAllByDocIdAndPatientId",
    responses={
        200: {"model": AppointmentPagedResultDto, "description": "Success"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["Appointments"],
    response_model_by_alias=True,
)
async def appointments_get_all_by_doc_id_and_patient_id_get(
    patient_id: str = Query(None, description=""),
    doctor_id: str = Query(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> AppointmentPagedResultDto:
    ...


@router.get(
    "/Appointments/getAllByDocId",
    responses={
        200: {"model": AppointmentPagedResultDto, "description": "Success"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["Appointments"],
    response_model_by_alias=True,
)
async def appointments_get_all_by_doc_id_get(
    doctor_id: str = Query(None, description=""),
    date: str = Query(None, description=""),
) -> AppointmentPagedResultDto:
    ...


@router.get(
    "/Appointments/getAll",
    responses={
        200: {"model": AppointmentPagedResultDto, "description": "Success"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["Appointments"],
    response_model_by_alias=True,
)
async def appointments_get_all_get(
    patient_id: str = Query(None, description=""),
    date: str = Query(None, description=""),
    order: str = Query(None, description=""),
    limit: int = Query(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> AppointmentPagedResultDto:
    ...


@router.get(
    "/Appointments/get",
    responses={
        200: {"model": AppointmentDto, "description": "Success"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
        422: {"model": MessageDto, "description": "Invalid Inputs"},
    },
    tags=["Appointments"],
    response_model_by_alias=True,
)
async def appointments_get_get(
    id: str = Query(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> AppointmentDto:
    ...


@router.get(
    "/Appointments/getPatientLatestAppointments",
    responses={
        200: {"model": AppointmentPagedResultDto, "description": "Success"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["Appointments"],
    response_model_by_alias=True,
)
async def appointments_get_patient_latest_appointments_get(
    patient_id: str = Query(None, description=""),
    date: str = Query(None, description=""),
    time: str = Query(None, description="hhmm format"),
    limit: int  = Query(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> AppointmentPagedResultDto:
    ...


@router.get(
    "/Appointments/getSlots",
    responses={
        200: {"model": AppointmentsGetSlotsGet200Response, "description": "Success"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
        422: {"model": MessageDto, "description": "Invalid Inputs"},
    },
    tags=["Appointments"],
    response_model_by_alias=True,
)
async def appointments_get_slots_get(
    doctor_id: str = Query(None, description=""),
    date: str = Query(None, description=""),
) -> AppointmentsGetSlotsGet200Response:
    ...


@router.get(
    "/Appointments/getStandardSlots",
    responses={
        200: {"model": AppointmentsGetSlotsGet200Response, "description": "Success"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
        422: {"model": MessageDto, "description": "Invalid Inputs"},
    },
    tags=["Appointments"],
    response_model_by_alias=True,
)
async def appointments_get_standard_slots_get(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> AppointmentsGetSlotsGet200Response:
    ...


@router.put(
    "/Appointments/update",
    responses={
        200: {"model": AppointmentForUpdateDto, "description": "Success"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
        422: {"model": MessageDto, "description": "Invalid Inputs"},
    },
    tags=["Appointments"],
    response_model_by_alias=True,
)
async def appointments_update_put(
    appointment_for_update_dto: AppointmentForUpdateDto = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> AppointmentForUpdateDto:
    ...
