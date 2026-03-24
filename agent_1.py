#with memory tool added
import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai.types import Content, Part
from dotenv import load_dotenv

load_dotenv()

flight_agent = LlmAgent(
    model = "gemini-2.5-flash",
    name = "Flight_Agent",
    description = """
        Your departute city is {departure}.
        Tell me the optimal route between the flights.
        """,
    tools = [PreloadMemoryTool()] #loads up the memory if its exist
)

runner = InMemoryRunner(agent = flight_agent, app_name = "agents") #creating it own inmemory services, runs everything locally in memory
    
async def run_dialogue():
    #First session:  user gives some info
    session_id = "session_1"

    # Create the session first
    await runner.session_service.create_session(
        app_name = runner.app_name,
        user_id = 'user1',
        session_id = session_id,
    )

    print(f"User: Im travelling to India.")
    content = Content(role = "user", parts = [Part(text = "Im travelling to India")])

    async for event in runner.run_async(user_id = "user1", session_id = session_id, new_message = content):
        # to check if the event has content and is from the agent and not the user.
        if event.content and event.content.parts and event.author != "user":
            for part in event.contents.parts:
                if part.text:
                    print(f"Agent: {part.text}")

    # after each conversation, save it to the memory, within the session we created earlier
    #this below code retrieves the seeion we created
    session = await runner.session_service.get_session(
        app_name = runner.app_name,
        user_id = "user1",
        session_id = session_id
    )

    await runner.memory_service.add_seesion_to_memory(session)


asyncio.run(run_dialogue())