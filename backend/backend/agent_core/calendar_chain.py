from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool, tool
from .calendar_tools import list_calendar_list, list_calendar_events, create_calendar_list, insert_calendar_event
import os
from dotenv import load_dotenv

load_dotenv()

class CalendarAgent:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.agent = self._create_agent()
        

    def run(self, messages):
        return self.agent.invoke(input=messages)

    
    def get_calendar_list(self, max_capacity=50) -> str:
        """Lists all available calendars."""
        calendars = list_calendar_list(
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            max_capacity=max_capacity
        )
        return str(calendars)

    def get_calendar_events(self, **kwargs) -> str:
        """Lists events from a specific calendar."""
        calendar_id = kwargs.get("calendar_id", "primary")  # Default to 'primary'
        max_capacity = int(kwargs.get("max_capacity", 10))  # Default to 10
        events = list_calendar_events(
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            calendar_id=calendar_id,
            max_capacity=max_capacity
        )
        return str(events)

    def create_new_calendar(self, **kwargs) -> str:
        """Creates a new calendar with the given name."""
        calendar_name = kwargs.get("calendar_name")
        if not calendar_name:
            return "Error: 'calendar_name' is required."
        calendar = create_calendar_list(
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            calendar_name=calendar_name
        )
        return str(calendar)

    def create_calendar_event(self, **kwargs) -> str:
        """Creates a new event in the specified calendar."""
        calendar_id = kwargs.get("calendar_id", "primary")  # Default to 'primary'
        event_details = kwargs.get("event_details")
        if not event_details:
            return "Error: 'event_details' is required."
        event = insert_calendar_event(
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            calendar_id=calendar_id,
            event_details=event_details
        )
        return str(event)

    def _create_agent(self):
        # Define tools
        tools = [
            Tool(
                name="get_calendar_list",
                func=self.get_calendar_list,
                description="Lists all available calendars in the user's Google Calendar account. "
                            "Arguments: max_capacity (int) - Maximum number of calendars to retrieve (default: 50)."
            ),
            Tool(
                name="get_calendar_events",
                func=self.get_calendar_events,
                description="Retrieves events from a specific calendar. "
                            "Arguments: calendar_id (str) - ID of the calendar (default: 'primary'); "
                            "max_capacity (int) - Maximum number of events to retrieve (default: 10)."
            ),
            Tool(
                name="create_new_calendar",
                func=self.create_new_calendar,
                description="Creates a new calendar with the specified name. "
                            "Arguments: calendar_name (str) - Name of the new calendar."
            ),
            Tool(
                name="create_calendar_event",
                func=self.create_calendar_event,
                description="Creates a new event in a specific calendar. "
                            "Arguments: calendar_id (str) - ID of the calendar (default: 'primary'); "
                            "event_details (dict) - Details of the event to create."
            )
        ]

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful agent who is equipped with a variety of Google Calendar functions to handle Google calendar related tasks.

            1. Use get_calendar_list function to retrieve a list of calendars that are available in your Google Calendar account.
            - Example usage: get_calendar_list(max_capacity=50) with default capacity of 50 calendars unless user stated otherwise. Pass as an integer only

            2. Use get_calendar_events function to retrieve a list of events from a specific calendar.
                - Example usage: get_calendar_events(calendar_id='primary', max_capacity=10) with default capacity of 10 events unless user stated otherwise.
                - If you want to retrieve events from a specific calendar, you can specify the calendar_id parameter.
                    calendar_list = get_calendar_list(max_capacity=50)
                    search calendar id from calendar_list
                    get_calendar_events(calendar_id='calendar_id', max_capacity=10)

            3. Use create_new_calendar function to create a new calendar.
                - Example usage: create_new_calendar(calendar_name='My calendar')
                - This function will create a new calendar with the specified name.

            4. Use create_calendar_event function to create a new event in a specific calendar.
                Here is a basic example:
                event_details = {{
                    'summary': 'Meeting',
                    'location': 'Office',
                    'description': 'Team meeting',
                    'start': {{
                        'dateTime': '2024-03-20T09:00:00-07:00',
                        'timeZone': 'America/Los_Angeles',
                    }},
                    'end': {{
                        'dateTime': '2024-03-20T10:00:00-07:00',
                        'timeZone': 'America/Los_Angeles',
                    }},
                    'attendees': [
                        {{'email': 'colleague@example.com'}},
                    ]
                }}

                Use primary calendar if user didn't specify a calendar:
                create_calendar_event(calendar_id='primary', event_details=event_details)
                
            Please keep in mind the code is write on Python syntax. For example, true should be True
            Always format dates and times properly when creating events.
            When creating events, ensure all required fields are included."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Initialize LLM
        llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0,
            api_key=os.getenv('OPENAI_API_KEY')
        )

        # Create agent
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        return agent_executor



