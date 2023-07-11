# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class Filter(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Filter - a model defined in OpenAPI

        op: The op of this Filter [Optional].
        col: The col of this Filter [Optional].
        val: The val of this Filter [Optional].
    """

    op: Optional[str] = Field(alias="op", default=None)
    col: Optional[str] = Field(alias="col", default=None)
    val: Optional[str] = Field(alias="val", default=None)

Filter.update_forward_refs()
