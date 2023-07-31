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
import nats
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError
# from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.patientDto import PatientDto
from openapi_server.models.message_dto import MessageDto
from dotenv import load_dotenv
from kafka import KafkaProducer
import os
# from kafka.admin import NewTopic
# from kafka import KafkaConsumer
# from nats.aio.client import Client as NATSClient
# from firebase_admin import firestore
import traceback
import json
from uuid import uuid4
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

kafka_server = "34.170.91.100:29092"
# kafka_server = os.getenv("KAFKA_SERVER")
# nats_server=os.getenv("NATS_SERVER")
nats_server="nats://35.232.2.210:4222"
router = APIRouter()
# producer = KafkaProducer(
#     bootstrap_servers=kafka_server,
#     client_id="my-app"
# )



@router.get(
    "/getAllpatients",
    responses={
        200: {"model": PatientDto, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["PatientsService"],
    summary="GetAll Patients",
    response_model_by_alias=True,
)
async def getallpatients(
    patientId: str = Query(None, description=""),
) -> PatientDto :
    try:
        # nats_server=
        print(os.getenv("NATS_SERVER"))
        nc = await nats.connect(nats_server)
        data={
             "patientId":patientId,
             "type":"getAll"
        }
        ddata=json.dumps(data)
        response = await nc.request("Patient", (ddata).encode(), timeout=500)
        print("Received response: {message}".format(
            message=response.data.decode()))
        print(response.data.decode())
        stringdata=response.data.decode()
        # json_str_modified = stringdata.replace('true', 'True')
        res: PatientDto = stringdata
        result = json.loads(res)
        return result
    except TimeoutError:
        print("Request timed out")
        return {
                    "status": 404,
                    "body": "Request timed out",
                }
    except Exception as e:
         print(e)
         return {
                    "status": 404,
                    "body": str(e),
                }

@router.post(
    "/CreatePatients",
    responses={
        200: {"model": PatientDto, "description": "Successful response"},
        401: {"model": MessageDto, "description": "Unauthorized"},
        404: {"model": MessageDto, "description": "The specified resource was not found"},
    },
    tags=["PatientsService"],
    summary="Create patient",
    response_model_by_alias=True,
)
async def createPatients(
    patientdata: PatientDto = Body(None, description=""),
) -> PatientDto :
    try:
            
            patientdata.patientId= str(uuid4())
            request=patientdata.dict()
            print(type(request))
            if not request:
                raise ValueError("invalid-inputs")
            
            Request = json.loads(json.dumps(request))

            try:
                print(kafka_server)
                producer = KafkaProducer(
                            bootstrap_servers=kafka_server,
                            client_id="my-app"
                        )
                outgoingMessage = {
                    "key": f"create#{patientdata.patientId}",
                    "value": json.dumps({
                        **Request,
                        "isExist": True,
                        "createdAt":datetime.datetime.utcnow().isoformat(),
                    }),
                }
                try:
                    future = producer.send("Patient", key=(outgoingMessage["key"]).encode(), value=(outgoingMessage["value"]).encode())
                    print("Message sent successfully!",future)
                except Exception as e:
                    traceback.print_exc()
                    raise ValueError("Failed to send message")
                    # print("Failed to send message:", repr(e))
                return JSONResponse(
            status_code=202,
            content={
               "status":202,
               "body": request
          },
        )
            except Exception as error:
                traceback.print_exc()
                if str(error).find("no-patientId-found") != -1:
                    raise ValueError("no-patientId-found")
                raise error
    except Exception as error:
            traceback.print_exc()
            print(error)
            return JSONResponse(
            status_code=404,
            content={
               "status":404,
               "body":"something went worng"
          },
        )
@router.put("/updatePatient",
               responses={
                    200:{"model":PatientDto,"description":"Sucessful response"},
                    401: {"model": MessageDto, "description": "Unauthorized"},
                    404: {"model": MessageDto, "description": "The specified resource was not found"},
               },
               tags=["PatientsService"],
               summary="update patient data",
               response_model_by_alias=True,
)
async def updatedata(patientdata: PatientDto = Body(None, description=""),) -> PatientDto:
     try:
          producer = KafkaProducer(
                            bootstrap_servers=kafka_server,
                            client_id="my-app"
                        )
          res= await getallpatients(patientdata.patientId)
          print("is patient exits",res)
          if(len(res)==0):
               raise Exception("No-patient-found")
          request=patientdata.dict()
          print(type(request))
          if not request:
                raise ValueError("invalid-inputs")
            
          Requestdata = json.loads(json.dumps(request))
          outgoingMessage = {
                    "key": f"update#{patientdata.patientId}",
                    "value": json.dumps({
                        **Requestdata,
                        "isExist": True,
                        "createdAt":datetime.datetime.utcnow().isoformat(),
                    }),
                }
          try:
                future = producer.send("Patient", key=(outgoingMessage["key"]).encode(), value=(outgoingMessage["value"]).encode())
                print("Message sent successfully!",future)
          except Exception as e:
                traceback.print_exc()
                raise ValueError("Failed to send message")
                    # print("Failed to send message:", repr(e))
          return JSONResponse(
            status_code=201,
            content={
               "status":201,
               "body":request
          },
        )
     except Exception as e:
          traceback.print_exc()
          return JSONResponse(
            status_code=404,
            content={
               "status":404,
               "body":str(e)
          },
        )
@router.delete("/deletePatient",
                responses={
                    200:{"model":PatientDto,"description":"Sucessful response"},
                    401: {"model": MessageDto, "description": "Unauthorized"},
                    404: {"model": MessageDto, "description": "The specified resource was not found"},
               },
               tags=["PatientsService"],
               summary="update patient data",
               response_model_by_alias=True,
)
async def deletepatient(patientId: str = Query(..., description=""),) -> PatientDto:
     try:
          res=await getallpatients(patientId)
          if(len(res)==0):
               raise Exception("No-patient-found")
          producer = KafkaProducer(
                            bootstrap_servers=kafka_server,
                            client_id="my-app"
                        )
          outgingMessage={
               "key":f"delete#{patientId}",
               "value": json.dumps({
                        "isExist": False,
                        "createdAt":datetime.datetime.utcnow().isoformat(),
                    }),
          }
          try:
               message=producer.send("Patient",key=outgingMessage["key"].encode(),value=outgingMessage["value"].encode())
               print("message send",message)
          except:
               traceback.print_exc()
               raise Exception("failed to send data")
          return JSONResponse(
            status_code=201,
            content={
               "status":201,
               "body":"Patient data deleted"
          },
        )
     except Exception as e:
          print(e)
          return JSONResponse(
            status_code=404,
            content={
               "status":404,
               "body":str(e)
          },
        )