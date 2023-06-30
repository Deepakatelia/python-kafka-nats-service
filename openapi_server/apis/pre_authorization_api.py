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
from openapi_server.models.message_dto import MessageDto
from openapi_server.models.preauthorization_dto import PreauthorizationDto
from openapi_server.models.textpreauthorization import Textpreauthorization
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = "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"

router = APIRouter()


@router.post(
    "/preauthorization",
    responses={
        200: {"model": PreauthorizationDto, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["PreAuthorization"],
    summary="Match the user input to the PreAuthorization schema.",
    response_model_by_alias=True,
)
async def preauthorization_post(
    textpreauthorization: Textpreauthorization = Body(None, description=""),
) -> PreauthorizationDto:
    try:
        rules={
            "for CT-scan":{
                "report":"CT-Scan"
            },
            "for MRI":{
                "report":"MRI"
            },
            "for Ultrasound Imaging":{
                "report":"Ultrasound"
            },
            "for X-ray :":{
                "report":"X-ray"
            }

        }
        existing_chats=[
                        {"role": "user", "content": "Generate pre-authorization notes for a CT - Scan"},
                        {"role": "assistant", "content": "I'm sorry, I cannot generate pre-authorization notes for a CT-scan without Medical Necessity information. Please provide me with the Medical Necessity information to process your request."},
                        {"role": "user", "content": "make sure you get the Medical Necessity input  from user once you recive Medical Necessity data from the user return response as json like {\"report\":\"string\",\"Medical_Necessity\":\"string\"} and fellow entity rules"+str(rules)},
                        {"role": "assistant", "content": "sure"},
        ]
        print(textpreauthorization.text)
        for i in textpreauthorization.text:
            new_chat = {"role": i.role, "content": i.content}
            existing_chats.append(new_chat)
            
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = existing_chats,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            timeout=20
        )
        
        data=completion.choices[0].message.content
        
        # intent=checkintent(data)

        return JSONResponse(
            status_code=202,
            content={"role":"assistant","content":data,"intent":"preauthorization"},
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

