from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

def create_service_with_token(access_token, refresh_token, api_name, api_version):
    """
    Create a Google API service using the access token from frontend.
    
    Parameters:
        access_token: str - The access token from frontend OAuth
        api_name: str - The name of the API (e.g. 'calendar')
        api_version: str - The version of the API (e.g. 'v3')
    
    Returns:
        service: googleapiclient.discovery.Resource
    """
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        scopes=['https://www.googleapis.com/auth/calendar'],
    )

    try:
        service = build(api_name, api_version, credentials=creds, static_discovery=False)
        print(f'{api_name} {api_version} service created successfully')
        return service
    except Exception as e:
        print(f'Failed to create service: {e}')
        return None