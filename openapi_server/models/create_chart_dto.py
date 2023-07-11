# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from openapi_server.models.create_x_axis_dto import CreateXAxisDto
from openapi_server.models.create_y_axis_dto import CreateYAxisDto
from openapi_server.models.column_dto import ColumnDto
from openapi_server.models.filter import Filter


class CreateChartDto(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    CreateChartDto - a model defined in OpenAPI

        data_source: The data_source of this CreateChartDto [Optional].
        visualization: The visualization of this CreateChartDto [Optional].
        title: The title of this CreateChartDto [Optional].
        x_axis: The x_axis of this CreateChartDto [Optional].
        y_axis: The y_axis of this CreateChartDto [Optional].
        filters: The filters of this CreateChartDto [Optional].
    """

    data_source: Optional[str] = Field(alias="dataSource", default=None)
    visualization: Optional[str] = Field(alias="visualization", default=None)
    title: Optional[str] = Field(alias="title", default=None)
    x_axis: Optional[CreateXAxisDto] = Field(alias="xAxis", default=None)
    y_axis: Optional[List[CreateYAxisDto]] = Field(alias="yAxis", default=None)
    columns: Optional[List[ColumnDto]] = Field(alias="columns", default=None)
    filters: Optional[List[Filter]] = Field(alias="filters", default=None)

CreateChartDto.update_forward_refs()
