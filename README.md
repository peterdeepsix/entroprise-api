# Key

dd74decc-8825-4a49-b9bc-e4608249d612

# Local Development

py -3 -m venv entroprise-api

Scripts\activate

pip3 install -r requirements.txt

gcloud auth application-default login

#dev    
uvicorn main:app --reload

#prod
gunicorn main:app -c gunicorn_config.py

docker build -t us.gcr.io/$PROJECT_ID/cloud_run_fastapi .
docker run -p 8000:8000 -it us.gcr.io/$PROJECT_ID/cloud_run_fastapi:latest
docker push us.gcr.io/$PROJECT_ID/cloud_run_fastapi