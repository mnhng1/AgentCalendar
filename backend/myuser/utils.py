from oauth2client import client
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'config', 'client_secret.json')


def get_id_token_with_code_method_1(code):
    """
        Get the id token with the code from the user.
    
    Parameters:
        code: str - The code from the user.
    
    Returns:
        id_token: str - The id token of the user.
    """
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['profile',  'email', 'https://www.googleapis.com/auth/calendar'],
        code
    )
    id_token = credentials.id_token
    print(id_token)
    return id_token



def get_id_token_with_code_method_2(code):
    token_endpoint = 'https://oauth2.googleapis.com/token'
    payload = {
        'code':code,
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'grant_type':'authorization_code',
        'redirect_uri':'postmessage'
    }

    body = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}