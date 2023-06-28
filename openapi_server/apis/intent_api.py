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
from flask import jsonify
from starlette.responses import JSONResponse
import openai
import json
import traceback

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.intentresponse import Intentresponse
from openapi_server.models.message_dto import MessageDto
from openapi_server.models.textintent import Textintent
from openapi_server.models.text_schedule_appointments import TextScheduleAppointments
# from fastapi import FastAPI
from openapi_server.apis.schedule_appointments_api import schedule_appointments_post 
from openapi_server.apis.create_careplan_api import creategoal_post
from openapi_server.models.text_creategoal import TextCreategoal
from openapi_server.models.textpreauthorization import Textpreauthorization
from openapi_server.apis.pre_authorization_api import preauthorization_post

# router = APIRouter()
# app = FastAPI()
router = APIRouter()
# app.include_router(ScheduleAppointmentsApiRouter)
# client = TestClient(app)

# data = {"text_schedule_appointments": {"text": [{"role": "user", "content": "appointment"}]}}
# response = client.post("/ScheduleAppointments", json=data)
# print(response.json())


@router.post(
    "/extractintent",
    responses={
        200: {"model": Intentresponse, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["Intent"],
    summary="Return intent for user input",
    response_model_by_alias=True,
)
async def extractintent_post(
    textintent: Textintent = Body(None, description=""),
) -> Intentresponse:
    try:
        rules={
            "for appointments or schedule":{
                "intent":"appointment"
            },
            "for Labs or for Review labs":{
                "intent":"lab"
            },
            "for pre-authorization":{
                "intent":"preauthorization"
            },
            "for create  goal":{
                "intent":"goal"
            },
            "for Order prescription":{
                "intent":"prescription"
            },
            "for Dispatch educational material":{
                "intent":"educationalmaterial"
            }

        }
        openai.api_type = "azure"
        openai.api_base = "https://atelia.openai.azure.com/"
        openai.api_version = "2023-03-15-preview"
        openai.api_key = "241c592906b04cbca1be6703ee1089b8"
        completion = openai.ChatCompletion.create(
                    engine="DynamicDashboards",
                    messages = [
                        {"role": "user", "content": "Hello"},
                        {"role": "assistant", "content": "Based on the given intent generator rules, the intent in the text \"Hello\" cannot be identified as it does not match any of the specified intents.",},
                        {"role": "user", "content": "identify the intent in the text:" + str(textintent.text[0].content)+ "and make sure you follow the intent generator rules:"+str(rules)}],
                    temperature=0.7,
                    max_tokens=2054,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                    timeout=20
                    )
        data=completion.choices[0].message.content
        print(data)
        def checkintent(data):
            word_list = ['appointment', 'goal', 'preauthorization', 'lab',"prescription","educationalmaterial"]
            found_words = []
            for word in word_list:
                if word in data:
                    found_words.append(word)
            print(found_words)
            if len(found_words)!=0:
                return found_words[0]
            else:
                print("false")
                return False
        intent=checkintent(data)
        if intent=="appointment":
            text_schedule_appointments =TextScheduleAppointments(text=textintent.text)
            res= await schedule_appointments_post(text_schedule_appointments)
            response = json.loads(res.body.decode())
            print(type(response))
            response["intent"]="appointment"
            return JSONResponse(
            status_code=200,
            content=response,
            )
        elif intent=="goal":
            text_create_goal =TextCreategoal(text=textintent.text)
            res= await creategoal_post(text_create_goal)
            response = json.loads(res.body.decode())
            # print(response.content)
            response["intent"]="goal"
            print((response))

            return JSONResponse(
            status_code=200,
            content=response,
            )
        elif intent=="preauthorization":
            text_preauthorization =Textpreauthorization(text=textintent.text)
            res= await preauthorization_post(text_preauthorization)
            response = json.loads(res.body.decode())
            # print(response.content)
            response["intent"]="preauthorization"
            print((response))

            return JSONResponse(
            status_code=200,
            content=response,
            )
        elif intent==False:
            completion_general_bot = openai.ChatCompletion.create(
                    engine="DynamicDashboards",
                    messages = [
                        {"role": "user", "content": "when the user input was related to this input:\"what services you provide me\" give the this response \"As an AI language model,i can help you to schedule fellow up appointments,generate pre-authorisation notes,create goals under the plan,Dispatch educational material,Order prescription,Review labs\""},
                        {"role": "assistant", "content": "As an AI language model,i can help you to schedule fellow up appointments,generate pre-authorisation notes,create goals under the plan,Dispatch educational material,Order prescription,Review labs"},
                        {"role": "user", "content": str(textintent.text[0].content)}],
                    temperature=0.7,
                    max_tokens=2054,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                    timeout=20
                    )
            data_general=completion_general_bot.choices[0].message.content
            return JSONResponse(
            status_code=202,
            content={"role":"assistant","content":data_general},
        )

        return JSONResponse(
            status_code=402,
            content={"intent": intent},
        )
    except openai.error.AuthenticationError:
        return JSONResponse(
            status_code=401,
            content={"message": "AuthenticationError"},
        )
    except:
        traceback.print_exc()
        return JSONResponse(
            status_code=404,
            content={"message": "server error"},
        )
