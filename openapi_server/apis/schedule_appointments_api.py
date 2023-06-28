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
import datetime
from flask import jsonify
from starlette.responses import JSONResponse
import openai
import json
import traceback

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.appointment_dto import AppointmentDto
from openapi_server.models.message_dto import MessageDto
from openapi_server.models.text_schedule_appointments import TextScheduleAppointments
import asyncio

router = APIRouter()


@router.post(
    "/ScheduleAppointments",
    responses={
        200: {"model": AppointmentDto, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["ScheduleAppointments"],
    summary="Match the user input to the ScheduleAppointments schema.",
    response_model_by_alias=True,
)
async def schedule_appointments_post(
    text_schedule_appointments: TextScheduleAppointments = Body(None, description=""),
) -> AppointmentDto:
    try:
        openai.api_type = "azure"
        openai.api_base = "https://atelia.openai.azure.com/"
        openai.api_version = "2023-03-15-preview"
        openai.api_key = "241c592906b04cbca1be6703ee1089b8"

        current_datetime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
        datetime_obj = datetime.datetime.strptime(current_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Extract the date from the datetime object
        date = datetime_obj.date()

        existing_chats = [
            {"role":"system","content":"Assistant is an AI chatbot that helps users turn a natural language list into JSON format. After users input a list they want in JSON format, it will provide suggested list of attribute labels if the user has not provided any, then ask the user"},
            {"role":"user","content":"schedule a follow-up virtual appointment   on June 11th at 3 PM"},
            {"role":"assistant","content":"{\"id\": \"auto-generated\",\n  \"appointmentType\": 1,\n  \"appointmentDate\": \"2023-06-11\",\n  \"slotTime\": \"3 PM\",\n  \"symptoms\": \"headache and feeling ill\"}"},
            {"role": "user", "content": "what services you provide or how can you help me"},
            {"role": "assistant", "content": "I can help you with various tasks schedule a follow-up appointments and more."},
            {"role": "user", "content": " note current date was "+str(date)+" and appointmentDate,slotTime,symptoms and appointmentType=(1 if vitual apponitment else 2 for in-person visit)are required make sure you get it from user and make sure you didn't miss any fields while generating the response"},
            {"role": "assistant", "content": "Sure i make a note current date was"+str(date)+"and i generate dates accourding to this date"},
        ]
        # new_chat = [{"role": "user", "content": text_creategoal.text}]
        print(text_schedule_appointments.text)
        for i in text_schedule_appointments.text:
            new_chat = {"role": i.role, "content": i.content}
            existing_chats.append(new_chat)
        # print(existing_chats)
        async def callazureapi(data):
            completion = openai.ChatCompletion.create(
                        engine="DynamicDashboards",
                        messages = data,
                        temperature=0.7,
                        max_tokens=2054,
                        top_p=0.95,
                        frequency_penalty=0,
                        presence_penalty=0,
                        stop=None,
                        timeout=20
                        )
            return completion
        response = await asyncio.wait_for(callazureapi(existing_chats), timeout=1)
        data=response.choices[0].message.content
        print("response",data)

        return JSONResponse(
            status_code=202,
            content={"role":"assistant","content":data,"intent":"appointment"},
        )

        # return chart_data
    except openai.error.AuthenticationError:
        return JSONResponse(
            status_code=401,
            content={"message": "AuthenticationError"},
        )

    except TypeError:
        traceback.print_exc()
        return JSONResponse(
            status_code=404,
            content={"message": "invalid input: " },
        )
    except openai.error.InvalidRequestError:
        traceback.print_exc()
        return JSONResponse(
            status_code=404,
            content={"message": "invalid input: " },
        )
    except asyncio.TimeoutError:
        # Handle the timeout error
        return JSONResponse(
            status_code=404,
            content={"message": "time out"},
        )
    except:
        traceback.print_exc()
        return JSONResponse(
            status_code=404,
            content={"message": "server error"},
        )
