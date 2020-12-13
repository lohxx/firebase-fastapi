from fastapi import Request
from fastapi.security import APIKeyCookie

from starlette.exceptions import HTTPException

from firebase_admin import auth


class APICookieCustom(APIKeyCookie):
    """
        Valida o cookie, herda o APIKeyCookie para adicionar um 
        comportamento customizavel ao __call__
    """

    async def __call__(self, request: Request):
        session_cookie = request.cookies.get(self.model.name)
        try:
            decoded_claims = auth.verify_session_cookie(
                session_cookie, check_revoked=True)
        except (auth.InvalidSessionCookieError, ValueError):
            raise HTTPException(
                status_code=401,
                detail='Sua sessão expirou, por favor se logue novamente')