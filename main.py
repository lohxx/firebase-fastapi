import os
import logging

import requests

import firebase_admin

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from source.api import router as auth_router
from source.security.api_cookie import APICookieCustom

logger = logging.getLogger('uvicorn.error')

app = FastAPI()

app.include_router(auth_router, prefix='/auth')


@app.exception_handler(requests.exceptions.HTTPError)
async def http_exception_handle(request, exc):
    response_error_detail = exc.response.json()['error']

    return JSONResponse(
        status_code=response_error_detail['code'],
        content={'message': f'Não foi possível autenticar o usuário no firebase, motivo: {response_error_detail["message"]}'})


@app.get('/test', dependencies=[Depends(APICookieCustom(name="session"))])
async def search():
    # Testa a validação do cookie.
    return {'message': "ola mundo"}


@app.on_event("startup")
async def startup_event():
    firebase_admin.initialize_app()

    for env_var in ['FIREBASE_API_KEY', 'GOOGLE_APPLICATION_CREDENTIALS']:
        try:
            os.environ[env_var]
        except Exception:
            logger.warning(f'É necessario setar a env var {env_var} para que a api funcione corretamente.')