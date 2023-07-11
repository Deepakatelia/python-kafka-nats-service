# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class AppointmentsDeleteDelete200Response(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    AppointmentsDeleteDelete200Response - a model defined in OpenAPI

        patient_id: The patient_id of this AppointmentsDeleteDelete200Response [Optional].
        slot_id: The slot_id of this AppointmentsDeleteDelete200Response [Optional].
        message: The message of this AppointmentsDeleteDelete200Response [Optional].
    """

    patient_id: Optional[str] = Field(alias="patientId", default=None)
    slot_id: Optional[str] = Field(alias="slotId", default=None)
    message: Optional[str] = Field(alias="message", default=None)

AppointmentsDeleteDelete200Response.update_forward_refs()
