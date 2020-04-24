# flask app with ktrain and BERT

# create venv on windows

py -m venv venv

# activate on windows

.\venv\Scripts\activate

# deactivate

deactivate

# install deps

pip install -r requirements.txt

# setuo google cloud service account creds

\$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\arnol\code\entroprise-api\service-account-file.json"

# run flask app

flask run
