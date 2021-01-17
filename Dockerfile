# precisa de uma imagem do python que seja compativel com a versão do python suportada pelas libs.
FROM python:3.9
RUN apt-get update
RUN pip install pipenv
COPY . .
RUN pipenv install --system --deploy --ignore-pipfile
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

