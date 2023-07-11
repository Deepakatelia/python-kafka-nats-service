import httpx
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param
import json
class AuthenticationStrategy(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        scheme, credentials = get_authorization_scheme_param(request.headers.get("Authorization"))
        if not credentials or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = credentials

        try:
            async with httpx.AsyncClient() as client:
                # print(token)
                response = await client.get(
                    "https://auth-service-ao3vgcrk4q-uc.a.run.app/validateToken?access_token="+token
                )
                response.raise_for_status()
                data = response.json()
                # print(data)
                uId = data.get("uId")
                role = data.get("role")
                authId = data.get("auth0Id")

                if not authId:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No sub",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

                user = {
                    "uId": uId,
                    "authId": authId,
                    "role": role,
                }
                credentials = json.dumps(user)
                return HTTPAuthorizationCredentials(scheme="bearer", credentials=credentials)
        except httpx.HTTPError as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(error),
                headers={"WWW-Authenticate": "Bearer"},
            ) from error