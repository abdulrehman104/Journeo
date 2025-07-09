from typing import List
from decimal import Decimal
from agents import function_tool


# ———— Tools (simulated) ————————————————————————————————
@function_tool
def flight_search_tool(origin: str, destination: str, depart: str, return_date: str) -> List[dict]:
    print(
        f"[Tool: flight_search_tool] Called with {origin} → {destination}, {depart}–{return_date}")
    return [
        {"flight_no": "AI101", "price": 350.00, "airline": "AirExample"},
        {"flight_no": "EX202", "price": 420.00, "airline": "ExampleAir"},
        {"flight_no": "FL303", "price": 300.00, "airline": "FlyHigh"},
        {"flight_no": "SK404", "price": 500.00, "airline": "SkyTravel"},
        {"flight_no": "QT505", "price": 280.00, "airline": "QuickTrip"},
    ]


@function_tool
def hotel_search_tool(city: str, checkin: str, checkout: str) -> List[dict]:
    print(f"[Tool: hotel_search_tool] Called for {city}, {checkin}–{checkout}")
    return [
        {"hotel_name": "Hotel Alpha", "price_per_night": 80.00, "rating": 4.3},
        {"hotel_name": "Beta Suites", "price_per_night": 120.00, "rating": 4.7},
        {"hotel_name": "Gamma Inn", "price_per_night": 60.00, "rating": 3.9},
        {"hotel_name": "Delta Resort", "price_per_night": 200.00, "rating": 5.0},
        {"hotel_name": "Epsilon Lodge", "price_per_night": 90.00, "rating": 4.1},
    ]


@function_tool
def process_payment_tool(amount: Decimal, card_last4: str) -> dict:
    print(
        f"[Tool: process_payment_tool] Charging ${amount} to card ending {card_last4}")
    return {"status": "success", "amount_charged": amount, "transaction_id": "TXN123456"}