import datetime

from typing import Optional 

import firebase_admin
from firebase_admin import auth

from pydantic import BaseModel

from fastapi.responses import JSONResponse
from fastapi.security import APIKeyCookie
from fastapi import FastAPI, Response, Depends, Request

from source.models.user import User
from source.models.user import Authorization
from source.security.api_cookie import APICookieCustom
from source.firebase.main import sign_in_with_email_password

app = FastAPI()
default_app = firebase_admin.initialize_app()
cookie_scheme = APICookieCustom(name="session")


@app.post('/register')
async def register(user: User):
    try:
        user = auth.create_user(
            disabled=False,
            email=user.email,
            email_verified=False,
            password=user.password,
            display_name=user.name,
            phone_number=user.phone_number)
    except ValueError as e:
        # Alguma regra de validação do firebase foi quebrada
        return JSONResponse(
            status_code=400,
            content={'message': ''.join(e.args)})

    except firebase_admin._auth_utils.EmailAlreadyExistsError:
        # Usuario com algumas das chaves unicas já existe na base
        return JSONResponse(
            status_code=409,
            content={'message': 'O e-mail informado já esta associado a outro usuario'})

    except firebase_admin._auth_utils.PhoneNumberAlreadyExistsError:
        return JSONResponse(
            status_code=409,
            content={'message': 'O número de telefone informado já esta associado a outro usuario'})

    return {'message': 'Usuario criado com sucesso'}    


@app.get('/logout')
def logout():
    pass


@app.post('/login')
async def check_user(auth_infos: Authorization, response: Response):
    """
    Cria um cookie de sessão para um usuario valido.

    Args:
        auth_infos (Authorization): informações necessarias para autenticar
        um usuario no firebase, nesse caso é email e senha.

        response (Response): Objeto response que vai ser devolvido para o cliente.

    Returns:
        dict: dicionario informando que o login foi bem sucedido.
    """

    user_metadata = sign_in_with_email_password(auth_infos)

    id_token = user_metadata['idToken']

    expires_in = datetime.timedelta(days=5)
    try:
        session_cookie = auth.create_session_cookie(
            user_metadata['idToken'],
            expires_in=expires_in)

        expires = datetime.datetime.now() + expires_in

        response.set_cookie(
            key="session",
            value=session_cookie)

        return {'message': 'Logado com sucesso'}
    except Exception:
        pass


@app.get('/search')
async def search(cookie: str = Depends(cookie_scheme)):
    # Testa a validação do cookie.
    return {'message': "conseguiu ver o conteudo, ta logado"}