# Third Party Library
# Standard Library
from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt  # type: ignore


class Auth0HTTPBearer(HTTPBearer):
    async def __call__(self, request: Request):
        return await super().__call__(request)


class AuthCustom:
    def __init__(self):
        # pass
        self.implicit_scheme = None

    def get_user(self, creds: Optional[HTTPAuthorizationCredentials] = Depends(Auth0HTTPBearer(auto_error=False))):
        if creds:
            token = creds.credentials
            unverified_header = jwt.get_unverified_claims(token)
            return {
                "email_verified": unverified_header.get("email_verified", False),
                "name": unverified_header.get("name", None),
                "given_name": unverified_header.get("given_name", None),
                "family_name": unverified_header.get("family_name", None),
                "preferred_username": unverified_header.get("preferred_username", None),
                "email": unverified_header.get("email", None),
                "sub": unverified_header.get("sub", None),
                "role": unverified_header.get("role", None),
            }
        raise HTTPException(403, detail="Missing bearer token")


auth_user = AuthCustom()
