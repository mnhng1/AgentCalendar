import json
from google_apis import create_services

client_secret = 'client_secret.json'

def construct_google_calendar_client(client_secret):
    """
        Construct a Google Calendar client.
    
    Parameters:
        client_secret: str - The client secret file path.
    
    Returns:
        service: googleapiclient.discovery.Resource - The Google Calendar service.
    """

    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    service = create_services(client_secret, API_NAME, API_VERSION, SCOPES)
    return service 


calendar_service = construct_google_calendar_client(client_secret)

def create_calendar_list(calendar_name):
    """
        Create a new calendar list.
    
    Parameters:
        calendar_name: str - The name of the new calendar list.
    
    Returns:
        calendar: dict - The created calendar list.
    """
    calendar_list = {
    'summary': calendar_name,
   }

    create_calendar_list = calendar_service.calendars().insert(body=calendar_list).execute()
    return create_calendar_list