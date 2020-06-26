# key

dd74decc-8825-4a49-b9bc-e4608249d612

#### Local Development

pip3 install -r requirements.txt
# running with uvicorn, recommended for development
uvicorn main:app --reload
# running with gunicorn, recommended for production
gunicorn main:app -c gunicorn_config.py

gcloud auth application-default login

docker build -t us.gcr.io/$PROJECT_ID/cloud_run_fastapi .
docker run -p 8000:8000 -it us.gcr.io/$PROJECT_ID/cloud_run_fastapi:latest
docker push us.gcr.io/$PROJECT_ID/cloud_run_fastapi
