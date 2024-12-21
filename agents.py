from swarm import Agent
from prompts import calendar_agent_system_prompt, main_agent_system_prompt
from calendar_tools import list_calendar_list, list_calendar_events, create_calendar_list, insert_calendar_event

MODEL = 'gpt-4o-mini'

def transfer_to_main_agent():
    return main_agent


def transfer_to_calendar_agent():
    return calendar_agent

main_agent = Agent(
    name='Main Agent',
    prompt=main_agent_system_prompt,
    model=MODEL,
    function=transfer_to_calendar_agent
)

calendar_agent = Agent(
    name='Calendar Agent',
    prompt=calendar_agent_system_prompt,
    model=MODEL,
    functions=[
        transfer_to_main_agent
    ]
)

calendar_agent.functions.extend([list_calendar_events, list_calendar_list, create_calendar_list, insert_calendar_event])