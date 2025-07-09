import os 
from agents import AsyncOpenAI, set_tracing_disabled, OpenAIChatCompletionsModel


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
flight_agent=OpenAIChatCompletionsModel(model="gemini-1.5-pro", openai_client=client)
hotel_agent=OpenAIChatCompletionsModel(model="gemini-1.5-flash", openai_client=client)
payment_agent=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
set_tracing_disabled(True)
