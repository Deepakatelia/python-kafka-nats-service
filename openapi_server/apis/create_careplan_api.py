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
import os


from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.creategoal_dto import CreategoalDto
from openapi_server.models.message_dto import MessageDto
from openapi_server.models.text_creategoal import TextCreategoal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai.api_key = "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"

router = APIRouter()


@router.post(
    "/Creategoal",
    responses={
        200: {"model": CreategoalDto, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["CreateCareplan"],
    summary="Map the user input with Creategoal schema.",
    response_model_by_alias=True,
)
async def creategoal_post(
    text_creategoal: TextCreategoal = Body(None, description=""),
) -> CreategoalDto :
    try:
        current_datetime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
        # datetime_obj = datetime.fromisoformat(current_datetime)
        # Parse the string into a datetime object
        datetime_obj = datetime.datetime.strptime(current_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Extract the date from the datetime object
        date = datetime_obj.date()
        # print(date)
        existing_chats = [
            {"role":"system","content":"Assistant is an AI chatbot that helps users turn a natural language list into JSON format. After users input a list they want in JSON format, it will provide suggested list of attribute labels if the user has not provided any, then ask the user"},
            {"role": "user", "content": "add goal named 'bp to be reduced to 90' for plan 'Bp_Plan' within duration of two months with low priority to the patient 'JohnSon'"},
            {"role": "assistant", "content": "{ \"goalId\": \"auto-generated\", \"goalName\": \"bp to be reduced to 90\", \"goalPriority\": \"LOW\", \"goalStartDate\": \"yyyy-mm-dd\", \"goalTargetDate\": \"yyyy-mm-dd\",  \"patientName\": \"JohnSon\", \"planName\": \"Bp_Plan\" }"},
            {"role": "user", "content": "generate dates accourding to this date  "+str(date)+" and goalStartDate,goalTargetDate,goalName,planName,goalPriority are required make sure you get it from user and make sure you didn't miss any fields while generating the response"},
            {"role": "assistant", "content": "sure i make a note curent date ="+str(date)+ "and i ask the user for details untill the required feilds are given by user "},
            {"role": "user", "content": "what services you provide or how can you help me"},
            {"role": "assistant", "content": "I can help you with various tasks create goals and more."},
        ]
        # new_chat = [{"role": "user", "content": text_creategoal.text}]
        for i in text_creategoal.text:
            new_chat = {"role": i.role, "content": i.content}
            existing_chats.append(new_chat)
        print(current_datetime)

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=existing_chats,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            timeout=20
        )
        data=completion.choices[0].message.content
        return JSONResponse(
            status_code=202,
            content={"role":"assistant","content":data,"intent":"goal"},
        )

    #     # return chart_data
    except openai.error.AuthenticationError:
        return JSONResponse(
            status_code=401,
            content={"message": "AuthenticationError"},
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
