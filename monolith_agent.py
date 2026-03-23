import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from dotenv import load_dotenv

load_dotenv()

flight_agent = Agent(
    model = "gemini-2.5-flash",
    name = "Flight_Agent",
    description = "Tell me the best route between flights",
)

async def main():
    runner = InMemoryRunner(agent = flight_agent)
    events = await runner.run_debug("How many layovers are there between London and India?")


if __name__ == "__main__":
    asyncio.run(main())
