import os
import asyncio
from decimal import Decimal
from openai import AsyncOpenAI
from pydantic import BaseModel, field_validator
from journeo.all_agents import flight_agent, hotel_agent, payment_agent
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, ItemHelpers



# ———— ApiKey & Client Setup ————————————————————————————————
print("🔄 Loading API key and client…")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
set_tracing_disabled(True)
print("✅ AsyncOpenAI client configured, tracing disabled.")


# ———— Structured Output Models ————————————————————————————————
print("🔄 Defining Pydantic models…")


class FlightOption(BaseModel):
    flight_no: str
    airline: str
    price: Decimal


class HotelOption(BaseModel):
    hotel_name: str
    price_per_night: Decimal
    rating: float


class BookingConfirmation(BaseModel):
    selected_flight: FlightOption
    selected_hotel: HotelOption
    total_cost: Decimal
    payment_status: str
    transaction_id: str

    @field_validator("total_cost", mode="before")
    @classmethod
    def calc_total(cls, v, info):
        print("[Model] Calculating total_cost from selected_flight and selected_hotel")
        data = info.data
        if "selected_flight" in data and "selected_hotel" in data:
            flight = data["selected_flight"].price
            hotel = data["selected_hotel"].price_per_night
            return flight + hotel
        return v  # fallback to provided value if not both present


print("✅ Using Pydantic Models.")


# ———— Orchestrator Agent ————————————————————————————————
print("🔄 Configuring orchestrator agent…")

orchestrator = Agent(
    name="TravelPlanner",
    instructions=(
        "You are a travel planner. "
        "1) Call search_flights with origin, destination, depart, return_date. "
        "2) Present the cheapest option as selected_flight. "
        "3) Call search_hotels with city, checkin, checkout. "
        "4) Present the cheapest hotel as selected_hotel. "
        "5) Call make_payment with the sum of both prices and card_last4='1234'. "
        "6) Return the full booking confirmation JSON."
    ),
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    handoffs=[flight_agent, hotel_agent, payment_agent],
    output_type=BookingConfirmation
)
print("✅ Orchestrator (TravelPlanner) configured.")


# ———— Streaming Interaction ————————————————————————————————
async def run_agent(prompt: str):
    final_message = None
    try:
        print("User Prompt: ", prompt)
        result_stream = Runner.run_streamed(orchestrator, input=prompt)
        async for event in result_stream.stream_events():
            if event.type == "raw_response_event":
                continue
            elif event.type == "agent_updated_stream_event":
                print(f"Agent updated: {event.new_agent.name}")
                continue
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    print("-- Tool was called")
                elif event.item.type == "tool_call_output_item":
                    print(f"-- Tool output: {event.item.output}")
                elif event.item.type == "message_output_item":
                    final_message = ItemHelpers.text_message_output(event.item)
                    print(f"-- Message output:\n {final_message}")
                else:
                    pass
    except Exception as e:
        print("\n❌ Error during execution:", str(e))
        raise
    return final_message

if __name__ == "__main__":
    user_input = "I want to book a trip from Karachi to Dubai departing 2025-08-15 and returning 2025-08-20."
    asyncio.run(run_agent(user_input))
