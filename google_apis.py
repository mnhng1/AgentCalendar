import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def create_services(client_secret_file, api_name, api_version, *scopes, prefix =''):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    creds = None
    working_dir = os.getcwd()
    token_dir = 'token_files'
    token_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.json'

    '''Check if token file exists, if not create one'''

    if not os.path.exists((os.path.join(working_dir, token_dir))):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
        creds = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file))

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(os.path.join(working_dir, token_dir, token_file), 'w') as token:
            token.write(creds.to_json())

    '''Build the service'''
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovey=False)
        print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to connect to the {API_SERVICE_NAME} service')
        os.remove(o.path.join(working_dir, token_dir, token_file))
        return None