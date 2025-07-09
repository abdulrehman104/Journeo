from typing import List
from agents import Agent
from decimal import Decimal
from pydantic import BaseModel, field_validator
from journeo.llm import flight_agent, hotel_agent, payment_agent
from journeo.tools import flight_search_tool, hotel_search_tool, process_payment_tool


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
        flight = info.data["selected_flight"].price
        hotel = info.data["selected_hotel"].price_per_night
        return flight + hotel


print("✅ Using Pydantic Models.")


# ———— Specialist Agents ————————————————————————————————
print("🔄 Configuring specialist agents…")

flight_agent = Agent(
    name="FlightAgent",
    instructions="You are a flight search specialist. Use the flight_search_tool to return a list of flights.",
    model=flight_agent,
    tools=[flight_search_tool],
    output_type=List[FlightOption]
)
print("✅ Using FlightAgent.")


hotel_agent = Agent(
    name="HotelAgent",
    instructions="You are a hotel search specialist. Use the hotel_search_tool to return a list of hotels.",
    model=hotel_agent,
    tools=[hotel_search_tool],
    output_type=List[HotelOption]
)
print("✅ Using HotelAgent.")


payment_agent = Agent(
    name="PaymentAgent",
    instructions="You are a payment specialist. Use process_payment_tool to charge the customer.",
    model=payment_agent,
    tools=[process_payment_tool],
    output_type=BookingConfirmation
)
print("✅ Using PaymentAgent.")
