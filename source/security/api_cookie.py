from fastapi import Request
from fastapi.security import APIKeyCookie
from fastapi.responses import RedirectResponse

from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from firebase_admin import auth


class APICookieCustom(APIKeyCookie):
    """
        Valida o cookie, herda o APIKeyCookie para adicionar um 
        comportamento customizavel ao __call__
    """

    async def __call__(self, request: Request):
        session_cookie = request.cookies.get(self.model.name)

        if not session_cookie:
            return RedirectResponse('/login')

        try:
            decoded_claims = auth.verify_session_cookie(
                session_cookie, check_revoked=True)
        except auth.InvalidSessionCookieError:
            return RedirectResponse('/login')