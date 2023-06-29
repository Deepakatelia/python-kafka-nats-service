
# from openapi_server.models.extra_models import TokenModel  # noqa: F401
# from openapi_server.models.create_chart_dto import CreateChartDto
# from openapi_server.models.message_dto import MessageDto
# from openapi_server.models.textreportgenerator import Textreportgenerator
# coding: utf-8
import json
import os
import traceback
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
# import openai
from flask import jsonify
from starlette.responses import JSONResponse

from openapi_server.models.create_x_axis_dto import CreateXAxisDto
from openapi_server.models.create_y_axis_dto import CreateYAxisDto
from openapi_server.models.create_y_axis_dto import CreateYAxisDto
import openai
import datetime
from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.create_chart_dto import CreateChartDto
from openapi_server.models.message_dto import MessageDto
from openapi_server.models.textreportgenerator import Textreportgenerator
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
router = APIRouter()


@router.post(
    "/reportgeneratror",
    responses={
        200: {"model": CreateChartDto, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["Report-Generator"],
    summary="generate the report definition",
    response_model_by_alias=True,
)
async def reportgeneratror_post(
        text_report_generator: Textreportgenerator = Body(None, description=""),
) -> CreateChartDto:
    try:
        entity = {
            "for Spo2": {
                "dataSource": "Spo2",
            },
            "for temperatute": {
                "dataSource": "Temp",
            }, "for Weight": {
                "dataSource ": "Weight",
            },
            "for bp": {
                "dataSource ": "Bp",
            },
            "for Pulse": {
                "dataSource ": "Pulse",
            },
            "for Glucose": {
                "dataSource ": "Glucose",
            },
            "for Appointments": {
                "dataSource ": "Appointments",
                "visualization": "Tabular",
            },
            "for xAxis": {
                "columnName  ": "createdAt",
                "label": "Created At"
            }

        }
        res={
            "dataSource": "Appointments",
            "visualization": "Tabular",
            "title": "String",
                    "columns": [
                                {
                                    "columnName": "id",
                                    "label": "id"
                                },
                                {
                                    "columnName": "appointmentDate",
                                    "label": "appointmentDate"
                                },
                                {
                                    "columnName": "appointmentType",
                                    "label": "appointmentType"
                                },
                                {
                                    "columnName": "slotTime",
                                    "label": "slotTime"
                                },
                                {
                                    "columnName": "symptoms",
                                    "label": "symptoms"
                                },
                                {
                                    "columnName": "patientId",
                                    "label": "patientId"
                                },
                                {
                                    "columnName": "patientName",
                                    "label": "patientName"
                                },
                                {
                                    "columnName": "patientImageUrl",
                                    "label": "patientImageUrl"
                                },
                                {
                                    "columnName": "doctorId",
                                    "label": "doctorId"
                                },
                                {
                                    "columnName": "doctorName",
                                    "label": "doctorName"
                                },
                                {
                                    "columnName": "doctorImageUrl",
                                    "label": "doctorImageUrl"
                                }
                                ],
            "filters": [
                {
                "op": ">=",
                "col": "appointmentDate",
                "val": "2023-05-03"
                }
            ],
            }
        current_datetime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [{"role":"user","content":"create report definition for temperature vital over last 10 days "},
                                 {"role":"assistant","content":"{\n\"dataSource\": \"temperature_vital\",\n\"visualization\": \"line chart\",\n\"title\": \"Temperature Vital over Last 10 Days\",\n\"xAxis\": {\n\"columnName\": \"date\",\n\"label\": \"Date\"\n},\n\"yAxis\": [\n{\n\"columnName\": \"temperature\",\n\"label\": \"Temperature (°C)\",\n\"axisBorderColor\": \"#2F4F4F\",\n\"axisTextColor\": \"#2F4F4F\"\n}\n],\n\"filters\": [\n{\n\"op\": \">=\",\n\"col\": \"date\",\n\"val\": \"2021-10-01\"\n}\n]\n}"},
                                 {"role":"user","content":"use this entity rules for vitals"+str(entity)+"and make a note cuurentdatetime is"+current_datetime},
                                 {"role":"user","content":"create table for past 10 appoitments"},
                                 {"role":"assistant","content":str(res)},
                                 {"role":"assistant","content":"make sure \"visualization\" must be either \"line chart\" or \"Tabular\""},
                                 {"role":"user","content":text_report_generator.text}],
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            timeout=20
        )
        data=completion.choices[0].message.content
        # print("response",data)
        json_start = data.find("{")
        json_end = data.rfind("}")
        json_data = data[json_start : json_end + 1]

        # Parse the JSON data
        report_definition = json.loads(json_data)
        
        # chart_data = json.loads(completion.choices[0].message.content)
        # print("chartdata", chart_data)
        return JSONResponse(
            status_code=202,
            content=report_definition,
        )
        # return chart_data
    except openai.error.AuthenticationError:
        traceback.print_exc()
        return JSONResponse(
            status_code=401,
            content={"message": "AuthenticationError"},
        )
    except json.decoder.JSONDecodeError:
        # traceback.print_exc()
        try:
            # data_str = data.strip("```").strip()
                # Replace single quotes with double quotes
           valid_json = data.replace("'", "\"")
        #    print((valid_json))
           json_data = json.loads(valid_json)
        #    print(json_data)
           return JSONResponse(
                    status_code=202,
                    content=json_data,
           )
        except:
             traceback.print_exc()
             return JSONResponse(
                    status_code=404,
                    content=data,
            )

    except TypeError:
        traceback.print_exc()
        return JSONResponse(
            status_code=404,
            content={"message": "invalid input: " + data},
        )
    except:
        traceback.print_exc()
        return JSONResponse(
            status_code=404,
            content={"message": "server error"},
        )
