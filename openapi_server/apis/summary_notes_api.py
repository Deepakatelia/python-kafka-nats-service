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

openai.api_key = "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"
# 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

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.message_dto import MessageDto
from openapi_server.models.notes_inner import NotesInner
from openapi_server.models.summary import Summary


router = APIRouter()


@router.post(
    "/notessummary",
    responses={
        200: {"model": Summary, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["Summary-notes"],
    summary="summarize the notes",
    response_model_by_alias=True,
)
async def notessummary_post(
    notes_inner: List[NotesInner] = Body(None, description=""),
) -> Summary:
    try:
        openai.api_type = "azure"
        openai.api_base = "https://atelia.openai.azure.com/"
        openai.api_version = "2023-03-15-preview"
        openai.api_key = "241c592906b04cbca1be6703ee1089b8"
        completion = openai.ChatCompletion.create(
                    engine="DynamicDashboards",
                    messages = [{"role": "user", "content": " read all  notes and give me summary" + str(notes_inner)}],
                    temperature=0.7,
                    max_tokens=2054,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                    timeout=30
                    )
        data=completion.choices[0].message.content
        # print(completion.choices[0].message.content)
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
