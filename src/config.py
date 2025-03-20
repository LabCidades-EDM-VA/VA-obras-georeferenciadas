import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env, se existir
load_dotenv()

class Config:
    # Conta de serviço Google
    SERVICE_ACCOUNT_PROJECT_ID = os.getenv('SERVICE_ACCOUNT_PROJECT_ID')
    SERVICE_ACCOUNT_PRIVATE_KEY_ID = os.getenv('SERVICE_ACCOUNT_PRIVATE_KEY_ID')
    SERVICE_ACCOUNT_PRIVATE_KEY = os.getenv('SERVICE_ACCOUNT_PRIVATE_KEY')
    SERVICE_ACCOUNT_CLIENT_EMAIL = os.getenv('SERVICE_ACCOUNT_CLIENT_EMAIL')
    SERVICE_ACCOUNT_CLIENT_ID = os.getenv('SERVICE_ACCOUNT_CLIENT_ID')
    SERVICE_ACCOUNT_CLIENT_CERT_URL = os.getenv('SERVICE_ACCOUNT_CLIENT_CERT_URL')
    SERVICE_ACCOUNT_INFO = {
        "type": "service_account",
        "project_id": SERVICE_ACCOUNT_PROJECT_ID,
        "private_key_id": SERVICE_ACCOUNT_PRIVATE_KEY_ID,
        "private_key": str(SERVICE_ACCOUNT_PRIVATE_KEY).replace('\\n', '\n'),
        "client_email": SERVICE_ACCOUNT_CLIENT_EMAIL,
        "client_id": SERVICE_ACCOUNT_CLIENT_ID,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": SERVICE_ACCOUNT_CLIENT_CERT_URL
    }