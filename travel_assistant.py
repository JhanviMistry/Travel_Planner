# travel_assistant.py
import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner

# Load environment variables
load_dotenv()
# Make sure your .env contains: GOOGLE_API_KEY=YOUR_REAL_KEY

# Create the travel assistant agent
travel_agent = LlmAgent(
    name="travel_assistant",
    model="gemini-2.5-flash",
    instruction=(
        "You are a helpful travel assistant for TravelWise. "
        "Help customers plan trips and answer travel questions."
    )
)

async def interactive_chat():
    runner = InMemoryRunner(agent=travel_agent)
    
    print("Welcome to TravelWise Assistant! Type 'exit' to quit.")
    
    while True:
        user_input = input("User > ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        
        # Run the agent on the user input
        events = await runner.run_debug(user_input)
        
        # Print only the agent’s text responses (clean output)
        for event in events:
            if hasattr(event, "content") and event.content:
                response_text = "".join(part.text for part in event.content.parts)
                print("Travel Assistant >", response_text)

# Run the interactive chat loop
if __name__ == "__main__":
    asyncio.run(interactive_chat())