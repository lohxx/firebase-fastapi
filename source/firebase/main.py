import os
import json

import requests

from source.models.user import Authorization


def sign_in_with_email_password(authorization: Authorization):
    """
    Loga o usuario com email e senha na API do firebase.

    Args:
        auth_infos (AuthInfo): informações necessarias para
            o login no firebase

    Returns:
        dict: metadados do usuario.
    """

    response = requests.post(
        'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword',
        params={'key': os.environ["FIREBASE_API_KEY"]},
        data=json.dumps({
            'returnSecureToken': True,
            'email': authorization.email,
            'password': authorization.password})
    )

    response.raise_for_status()

    return response.json()
