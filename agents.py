from swarm import Agent
from prompts import calendar_agent_system_prompt
from calendar_tools import list_calendar_list, list_calendar_events, create_calendar_list, insert_calendar_event

MODEL = 'gpt-4o-mini'


 





calendar_agent = Agent(
    name='Calendar Agent',
    prompt=calendar_agent_system_prompt,
    model=MODEL,
    functions=[
    ]
)

calendar_agent.functions.extend([list_calendar_events, list_calendar_list, create_calendar_list, insert_calendar_event])