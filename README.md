


# firebase-fastapi
Integração com o serviço de autenticação do firebase usando python e fastapi. Essa API usa o esquema de autenticação de e-mail e senha.

# Como executar 
Para executar o código desse repositório é necessario ter um projeto valido no firebase.

## Instalação usando o pipenv

1. Clonar o repositório
2. rodar o comando pipenv install dentro do diretório onde o código foi clonado.

```bash
git clone git@github.com:lohxx/firebase-fastapi.git
cd firebase-fastapi 
pipenv install
```

## Execução do projeto.

Definir as seguintes variáveis de ambiente.
| Variáveis                      | descrição                                                                    |
|--------------------------------|------------------------------------------------------------------------------|
| API_KEY                        | api key do seu projeto, para autenticar seu usuário na API Rest do firebase. |
| GOOGLE_APPLICATION_CREDENTIALS | caminho das credenciais do seu projeto no firebase.                          |

Iniciar o servidor.
```bash

uvicorn main:app

```