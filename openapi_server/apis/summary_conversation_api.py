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
from openapi_server.models.conversation_dto import ConversationDto
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
    "/conversationsummary",
    responses={
        200: {"model": ConversationDto, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["Summary-conversation"],
    summary="Process patient-doctor conversation and generate summary",
    response_model_by_alias=True,
)
async def conversationsummary_post(
    conversation_inner: ConversationInner = Body(None, description=""),
    # conversation_inner: List[ConversationInner] = Body(None, description=""),
) -> ConversationDto:
    try:
        # print(conversation_inner)
        entities={
            "Subjective": {
                "Chief of Complaint(CC)": {
                "Symptoms": "",
                "Problem": "",
                "Condition": "",
                "Diagnosis": ""
                },
                "History of Present Illness (HPI)": {
                "Narrative of the patient symptoms": "generate 2 - 3 lines max if possible as bullet points"
                },
                "Past Medical History (PMH)": {
                "Conditions": "",
                "Surgeries": "",
                "Hospitalizations": ""
                },
                "Social History (SH)": {
                "Patient Lifestyle": "",
                "Smoke History": "",
                "Alcohol History": ""
                },
                "Family history (FH)": {
                "Patient's family's medical history": ""
                }
            },
            "Objective": {
                "Vital signs": {
                "Temperature": "",
                "Heart rate": "",
                "Respiratory rate": "",
                "Blood pressure": "",
                "Oxygen saturation": ""
                },
                "Physical exam findings": {
                "Appearance": "",
                "Lung": "",
                "Cardiac": "",
                "Abdominal": "",
                "Extremities": "",
                "Behavior": "",
                "Mental status": ""
                },
                "Laboratory and diagnostic test results": {
                "Laboratory": "",
                "Diagnostic Imaging": "",
                "Microbiology": ""
                }
            },
            "Assessment": "if any Diagnosis by doctor map here",
            "Plan": "make sure response as bullet points"
            }

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [
                 {"role":"system","content":"Assistant is an AI chatbot that helps the Doctors to make a jsondata for patient-doctor conversations and turn that conversation as mention:"+str(entities)+"return unmaped feilds as \"Not mentioned\""},
                {"role": "user", "content": "map the entities by analyse the conversation " + str(conversation_inner)}
                ],
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            timeout=20
             )
        data=completion.choices[0].message.content
        print(data)
        jsondata = json.loads(data)
        print(jsondata)
        return JSONResponse(
            status_code=202,
            content=jsondata,
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
