import datetime
import logging

from fastapi import APIRouter, Response
from fastapi.security import APIKeyCookie
from fastapi.responses import JSONResponse

from firebase_admin import auth

from source.models.user import User
from source.models.user import Authorization
from source.firebase.main import sign_in_with_email_password


logger = logging.getLogger()

router = APIRouter()


@router.post('/register')
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


@router.get('/logout')
def logout():
    pass


@router.post('/login')
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