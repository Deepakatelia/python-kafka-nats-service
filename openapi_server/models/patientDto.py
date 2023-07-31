# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class PatientDto(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    CreategoalDto - a model defined in OpenAPI

    status: Optional[str] = Field(alias="status", default=None)
    category: Optional[str] = Field(alias="category", default=None)
    patientName: Optional[str] = Field(alias="patientName", default=None)
    patientId: Optional[str] = Field(alias="patientId",default=None)
    type: Optional[str] = Field(alias="type",default=None)
    isExist: Optional[str] = Field(alias="isExist",default=None)
    """


    status: Optional[str] = Field(alias="status", default=None)
    category: Optional[str] = Field(alias="category", default=None)
    patientName: Optional[str] = Field(alias="patientName", default=None)
    patientId: Optional[str] = Field(alias="patientId",default=None)
    type: Optional[str] = Field(alias="type",default=None)
    isExist: Optional[str] = Field(alias="isExist",default=None)
PatientDto.update_forward_refs()