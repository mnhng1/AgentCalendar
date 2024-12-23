import json
from .google_apis import create_service_with_token

def create_calendar_service(access_token, refresh_token):
    """Create a calendar service for a specific user."""
    return create_service_with_token(
        access_token=access_token,
        refresh_token=refresh_token,
        api_name='calendar',
        api_version='v3'
    )

def create_calendar_list(access_token, refresh_token, calendar_name):
    """
        Create a new calendar list.
    
    Parameters:
        calendar_name: str - The name of the new calendar list.
    
    Returns:
        calendar: dict - The created calendar list.
    """
    calendar_service = create_calendar_service(access_token, refresh_token)
    calendar_list = {'summary': calendar_name}
    created_calendar = calendar_service.calendars().insert(body=calendar_list).execute()
    return created_calendar

def list_calendar_list(access_token, refresh_token, max_capacity=200):
    """
        List the calendar list until reaching max_capacity.
    
    Parameters:
        max_capacity: int - The maximum number of calendars to retrieve.
    
    Returns:
        calendar_list: list - The list of calendars with 'id', 'name', 'description'.
    """
    calendar_service = create_calendar_service(access_token, refresh_token)
    max_capacity = int(max_capacity)
    all_calendars_cleaned = []
    next_page_token = None
    capacity_count = 0

    while capacity_count < max_capacity:
        response = calendar_service.calendarList().list(
            maxResults=min(200, max_capacity - capacity_count),
            pageToken=next_page_token
        ).execute()
        calendars = response.get('items', [])
        for calendar in calendars:
            calendar_info = {
                'id': calendar['id'],
                'name': calendar['summary'],
                'description': calendar.get('description', 'No description')
            }
            all_calendars_cleaned.append(calendar_info)
            capacity_count += 1
            if capacity_count >= max_capacity:
                break
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return all_calendars_cleaned

def list_calendar_events(access_token, refresh_token, calendar_id='primary', max_capacity=10):
    """
        List the calendar events until total number of events reach max_capacity.
    
    Parameters:
        calendar_id: str - The calendar id from which to list events.
        max_capacity: int - The maximum number of events to retrieve, default is 10.
    
    Returns:
        events: list - The list of events.
    """
    calendar_service = create_calendar_service(access_token, refresh_token)
    max_capacity = int(max_capacity)
    all_events = []
    next_page_token = None
    capacity_count = 0

    while capacity_count < max_capacity:
        response = calendar_service.events().list(
            calendarId=calendar_id,
            maxResults=min(200, max_capacity - capacity_count),
            pageToken=next_page_token
        ).execute()
        events = response.get('items', [])
        for event in events:
            all_events.append(event)
            capacity_count += 1
            if capacity_count >= max_capacity:
                break
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return all_events

def insert_calendar_event(access_token, refresh_token, calendar_id, event_details):
    """
        Insert a new event into a calendar.
    
    Parameters:
        calendar_id: str - The calendar id to insert the event.
        event_details: dict - The event details.
    
    Returns:
        event: dict - The created event.
    """
    calendar_service = create_calendar_service(access_token, refresh_token)

    # If event_details is a JSON string, parse it; else assume it's a dict
    if isinstance(event_details, str):
        request_body = json.loads(event_details)
    else:
        request_body = event_details

    event = calendar_service.events().insert(calendarId=calendar_id, body=request_body).execute()
    print(f'Event created: {event.get("htmlLink")}')
    return event
