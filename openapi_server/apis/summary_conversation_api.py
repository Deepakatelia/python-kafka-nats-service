# coding: utf-8
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
import openai
from starlette.responses import JSONResponse



from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.conversation_inner import ConversationInner
from openapi_server.models.message_dto import MessageDto
from openapi_server.models.summary import Summary
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = "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"

router = APIRouter()


@router.post(
    "/conversationsummary",
    responses={
        200: {"model": Summary, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["Summary-conversation"],
    summary="Process patient-doctor conversation and generate summary",
    response_model_by_alias=True,
)
async def conversationsummary_post(
    conversation_inner: List[ConversationInner] = Body(None, description=""),
) -> Summary:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [{"role": "user", "content": "generate summary for conversation" + str(conversation_inner)}],
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
            content={"summary": data},
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
