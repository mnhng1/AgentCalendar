from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'config', 'client_secret.json')

def get_credentials_with_code(code):
    """
    Exchange authorization code for credentials.

    Parameters:
        code: str - The authorization code received from Google.

    Returns:
        credentials: Credentials object containing access and refresh tokens.
    """
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=['profile', 'email', 'https://www.googleapis.com/auth/calendar'],
        redirect_uri="postmessage"  # Ensure this matches your OAuth client settings
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return credentials