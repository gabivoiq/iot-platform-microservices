FROM python:3.9.1-alpine3.12
STOPSIGNAL SIGINT
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
ENTRYPOINT [ "python", "./main.py" ]
