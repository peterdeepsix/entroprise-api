# flask app with ktrain and BERT

# git
git config --global user.email "peter@deepsixdesign.com"
git config --global user.name "Peter Arnold"

# create venv on windows

py -m venv venv

# activate on windows

Set-ExecutionPolicy Unrestricted -Force

.\venv\Scripts\activate

# deactivate

deactivate

# install deps

pip install -r requirements.txt

# setuo google cloud service account creds

\$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\arnol\code\entroprise-api\service-account-file.json"

# run flask app

flask run
