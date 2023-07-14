# coding: utf-8
import traceback
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
from openapi_server.models.transcriptiondto import TranscriptionDto
from openapi_server.models.message_dto import MessageDto
from openapi_server.models.summary import Summary
from dotenv import load_dotenv
import os
import json
load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key ="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"

router = APIRouter()


@router.post(
    "/transcriptionlabel",
    responses={
        200: {"model": TranscriptionDto, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["transcription-labeling"],
    summary="Label the Speakers in the conversation to Patient and Physician",
    response_model_by_alias=True,
)
async def transcription_post(
    conversation_inner: ConversationInner = Body(None, description=""),
    # conversation_inner: List[ConversationInner] = Body(None, description=""),
) -> TranscriptionDto:
    try:
        # print(conversation_inner
        # schema={
        # "Physician": "",
        # "Patient": "",
        # "Physician": "",
        # "Patient": "",
        # }and return response as JSON by using this schema"+str(schema)+" ensure that  JSON data follows the proper JSON format.
        existingmessage=[
                 {"role":"system","content":"Assistant is an AI chatbot that helps to render the conversation as Patient and Physician"},
                {"role": "user", "content": "Label the conversation to patient and physician" +conversation_inner.text[0].content}
                ]
        print(conversation_inner.text[0].content)

        async def getdatafrom_azure(existingmessage):
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = existingmessage,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            timeout=20
             )
            return completion.choices[0].message.content
        response=await (getdatafrom_azure(existingmessage))
        print(response)
        # jsondata = json.loads(response)
        # print(jsondata)
        return JSONResponse(
            status_code=202,
            content={"Conversation":response},
        )
    except openai.error.AuthenticationError:
        return JSONResponse(
            status_code=401,
            content={"message": "AuthenticationError"},
        )
    except json.decoder.JSONDecodeError:
        traceback.print_exc()

        stringdata=str(response)
        data_with_double_quotes = stringdata.replace("'", "\"")
        jsondata = json.loads(data_with_double_quotes)
        return JSONResponse(
            status_code=202,
            content=jsondata,
        )
    except:
        traceback.print_exc()
        return JSONResponse(
            status_code=404,
            content={"message": "server error"},
        )
