import os
import json
import random
import sqlite3
import requests
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.prebuilt import create_react_agent


load_dotenv()

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API KEY is missing in .env file")

app = FastAPI()
sessions = {}

class Message(BaseModel):
    session_id : str
    message : str

    @field_validator(session_id)
    @classmethod
    def session_id_is_missing(cls, v):
        if not v.strip():
            raise ValueError("Session ID is missing")
        return v
    
    @field_validator(message)
    @classmethod
    def message_is_empty(cls, v):
        if not v.strip():
            raise ValueError("Message is empty")
        return v
    
restaurant = {
    "name": "Bella Italia",
    "opening_hours": "12 PM to 11 PM",
    "location": "Astoria, New York",
    "phone": "123-456-7890"
}

def init_db():
    connect = sqlite3.connect("restaurant.db")
    cursor = connect.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT,
            people INTEGER,
            special_requirement TEXT,
            reference INTEGER
        )
    """)
    connect.commit()
    connect.close()


llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    temperature = 0.2,
    max_tokens = 500,
    api_key = api_key
)

@tool
def read_menu():
    return None

@tool
def read_faq():
    return None


@tool
def save_reservation(name, date, time, people, reference, special_requirement):
    return None

@tool
def get_reservation(name):
    return None

@tool
def cancel_reservation(reference):
    return None


@tool
def get_weather(city):
    return None

@tool
def check_availability(date : str, time : str) -> str:
    """Checks if tables are available at a specific date and time.
    Use this before booking to verify availability.
    """
    return f"yes, we have tables are available on {date} at {time}."

@tool
def book_table(date: str, time: str, people: int, special_requirement: str = None) -> str:
    """Books a table at the restaurants.
    Use this when customer wants to make a reservation.
    Requires date, time and number of people.
    Maximum 8 people per table
    """

    if int(people) > 8:
        return "Sorry, maximum 8 people per table."
    if int(people) < 1:
        return "Please, provide a valid number of people"
    
    ref = random.randint(1000,9999)
    return f"Table booked! Reference number : {ref}. Date: {date}, Time: {time}, People: {people}."


tools = [
    read_menu,
    read_faq,
    check_availability,
    book_table,
    save_reservation,
    get_reservation,
    cancel_reservation,
    get_weather
]


restaurant = {
    "name": "Bella Italia",
    "opening_hours": "12 PM to 11 PM",
    "location": "Astoria, New York",
    "phone": "123-456-7890"
}


system_prompt = f"""You are Arda, a reliable assistant for Bella Italia restaurant.

REAL RESTAURANT DATA — only use this information:
- Name : {restaurant['name']}
- Opening hours: {restaurant['opening_hours']}
- Location: {restaurant['location']}
- Phone: {restaurant['phone']}

Tool usage rules:

Always use read_menu() for menu questions
Always use read_faq() for policy questions
Always call check_availability() before booking
Always call save_reservation() after book_table()
Use get_weather() if customer mentions weather

ANTI-HALLUCINATION RULES:
- Only confirm menu items listed above
- Never make up prices, availability or details
- If unsure use the appropriate tool

BOOKING STEPS:
1. UNDERSTAND - identify what customer needs
2. GATHER - collect date, time, people count
3. VALIDATE - check availability
4. EXECUTE - make the booking
5. CONFIRM - give complete confirmation

GUARDRAIL RULES:
- Only answer Bella Italia related questions
- If asked unrelated questions redirect politely
"""

agent = create_react_agent(llm, tools, prompt=system_prompt)

@app.post("/chat")
def ai_chat(message : Message):
    session_id = message.session_id

    if session_id not in sessions:
        sessions[session_id] = []

    sessions[session_id].append(HumanMessage(content=message.message))
    
    result = agent.invoke({
        "messages" : sessions[session_id]
    })

    ai_message = result["message"][-1]

    sessions[session_id].append(ai_message)

    return {"output": ai_message.content}
