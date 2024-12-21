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

def list_calendar_list(max_capacity=200):
    """
        List the calendar list until reach max_capacity.
    
    Parameters:
        max_capacity: int - The maximum number of calendars to retrieve.
    
    Returns:
        calendar_list: list - The list of calendars with 'id', 'name', 'description'.
    """
    if isinstance(max_capacity, str):
        max_capacity = int(max_capacity)
    
    all_calendars = []
    all_calendars_cleaned = []
    next_page_token = None
    capacity_count = 0

    while True:
        calendar_list = calendar_service.calendarList().list(
            maxResults=min(200, max_capacity - capacity_count),
            pageToken = next_page_token
        ).execute()
        calendars = calendar_list.get('items', [])
        all_calendars.extend(calendars)
        if capacity_count >= max_capacity:
            break
        next_page_token = calendar_list.get('nextPageToken')
        if not next_page_token:
            break
    for calendar in all_calendars:
        calendar_info = {
            'id': calendar['id'],
            'name': calendar['summary'],
            'description': calendar['description']
        }
        all_calendars_cleaned.append(calendar_info)
    
    return all_calendars_cleaned

def list_calendar_events(calendar_id='primary', max_capacity=10):
    """
        List the calendar events until total number events reach max_capacity.
    
    Parameters:
        calendar_id: str - The calendar id from which to list events.
        max_capacity: int - The maximum number of events to retrieve, default is 10.
    
    Returns:
        events: list - The list of events with. 
    """
    if isinstance(max_capacity, str):
        max_capacity = int(max_capacity)
    
    all_events = []
    next_page_token = None
    capacity_count = 0

    while True:
        events = calendar_service.events().list(
            calendarId=calendar_id,
            maxResults=min(200, max_capacity - capacity_count),
            pageToken = next_page_token
        ).execute()
        events = events.get('items', [])
        all_events.extend(events)
        if capacity_count >= max_capacity:
            break
        next_page_token = events.get('nextPageToken')
        if not next_page_token:
            break
    
    return all_events

def insert_calendar_event(calendar_id, **event_details):
    """
        Insert a new event into a calendar.
    
    Parameters:
        calendar_id: str - The calendar id to insert the event.
        event_details: dict - The event details.
    
    Returns:
        event: dict - The created event.
    """
    request_body = json.loads(event_details['event_details'])
    event = create_calendar_list.events().insert(calendarId = calendar_id, body = request_body).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    return event
