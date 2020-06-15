
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY ./app /app
COPY ./requirements.txt /app/requirements.txt
COPY ./credentials-firebase.json /app/credentials-firebase.json
ENV GOOGLE_APPLICATION_CREDENTIALS /app/credentials-firebase.json
WORKDIR /app
RUN pip install -r requirements.txt