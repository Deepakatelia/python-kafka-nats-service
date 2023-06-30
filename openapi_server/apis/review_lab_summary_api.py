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
import asyncio
from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.message_dto import MessageDto
from openapi_server.models.reviewlabpromt import Reviewlabpromt
from openapi_server.models.reviewlabsummary import Reviewlabsummary
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = "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"
router = APIRouter()


@router.post(
    "/Reviewlabsummary",
    responses={
        200: {"model": Reviewlabsummary, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["ReviewLabSummary"],
    summary="Summarize the Reviewlab data",
    response_model_by_alias=True,
)
async def reviewlabsummary_post(
    reviewlabpromt: Reviewlabpromt = Body(None, description=""),
) -> Reviewlabsummary:
    try:
        # openai.api_type = "azure"
        # openai.api_base = "https://atelia.openai.azure.com/"
        # openai.api_version = "2023-03-15-preview"
        # openai.api_key = "241c592906b04cbca1be6703ee1089b8"
        async def getdatafrom_azure(text):
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [{"role": "user", "content": "generate summary " + str(text)}],
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            timeout=20
            )
            return completion.choices[0].message.content
        try:
            response=await asyncio.wait_for(getdatafrom_azure(reviewlabpromt.promt),timeout=1)
            return JSONResponse(
            status_code=202,
            content={"summary": response},
        )
        except asyncio.TimeoutError:
        # Handle the timeout error
            return JSONResponse(
            status_code=202,
            content={"summary": "timeout"},
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

