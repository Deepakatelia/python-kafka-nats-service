# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class CreategoalDto(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    CreategoalDto - a model defined in OpenAPI

        created_at: The created_at of this CreategoalDto [Optional].
        goal_id: The goal_id of this CreategoalDto [Optional].
        goal_name: The goal_name of this CreategoalDto [Optional].
        is_completed: The is_completed of this CreategoalDto [Optional].
        progress: The progress of this CreategoalDto [Optional].
        updated_at: The updated_at of this CreategoalDto [Optional].
        goal_priority: The goal_priority of this CreategoalDto [Optional].
        goal_start_date: The goal_start_date of this CreategoalDto [Optional].
        goal_target_date: The goal_target_date of this CreategoalDto [Optional].
        is_exist: The is_exist of this CreategoalDto [Optional].
        patient_id: The patient_id of this CreategoalDto [Optional].
        plan_id: The plan_id of this CreategoalDto [Optional].
    """

    # created_at: Optional[datetime] = Field(alias="createdAt", default=None)
    # goal_id: Optional[str] = Field(alias="goalId", default=None)
    # goal_name: Optional[str] = Field(alias="goalName", default=None)
    # is_completed: Optional[bool] = Field(alias="isCompleted", default=None)
    # progress: Optional[float] = Field(alias="progress", default=None)
    # updated_at: Optional[datetime] = Field(alias="updatedAt", default=None)
    # goal_priority: Optional[str] = Field(alias="goalPriority", default=None)
    # goal_start_date: Optional[date] = Field(alias="goalStartDate", default=None)
    # goal_target_date: Optional[date] = Field(alias="goalTargetDate", default=None)
    # is_exist: Optional[bool] = Field(alias="isExist", default=None)
    # patient_id: Optional[str] = Field(alias="patientId", default=None)
    # plan_id: Optional[str] = Field(alias="planId", default=None)
    role: Optional[str] = Field(alias="role", default=None)
    content: Optional[str] = Field(alias="content", default=None)

CreategoalDto.update_forward_refs()