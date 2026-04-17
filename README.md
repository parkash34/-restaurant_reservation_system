# Bella Italia — Restaurant Reservation System

An AI powered restaurant reservation system built with FastAPI, LangGraph
and Groq AI. The agent handles bookings, menu inquiries, FAQ questions
and weather checks using a combination of database tools, file tools
and API tools.

## Features

- SQLite database — reservations stored permanently
- File tools — menu read from JSON, FAQs from text file
- API tool — real time weather via wttr.in
- Full booking flow — check availability, book, save to database
- Reservation management — retrieve and cancel bookings
- Multi-session memory — each customer has separate conversation history
- Anti-hallucination — agent uses tools instead of guessing
- Guardrails — only answers restaurant related questions

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend web framework |
| LangGraph | AI agent framework |
| LangChain | AI tooling |
| Groq API | AI language model provider |
| LLaMA 3.3 70B | AI model |
| SQLite | Reservation database |
| Pydantic | Data validation |
| python-dotenv | Environment variable management |

## Project Structure
```
bella-italia-reservation/
│
├── env/
├── main.py
├── menu.json
├── faq.txt
├── restaurant.db      ← created automatically
├── .env
└── requirements.txt
```

## Setup

1. Clone the repository
```
git clone https://github.com/yourusername/bella-italia-reservation
```

2. Create and activate virtual environment
```
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Create `.env` file and add your Groq API key
```
API_KEY=your_groq_api_key_here
```

5. Run the server
```
uvicorn main:app --reload
```

## API Endpoint

### POST /chat

**Request:**
```json
{
    "session_id": "user_1",
    "message": "Book a table for 4 tomorrow at 7 PM, my name is Ahmed"
}
```

**Response:**
```json
{
    "output": "Your table for 4 is booked for tomorrow at 7 PM. Reference: 4018."
}
```

## Available Tools

| Tool | Type | Description |
|---|---|---|
| `read_menu` | File | Reads menu from menu.json |
| `read_faq` | File | Reads FAQs from faq.txt |
| `check_availability` | Logic | Checks table availability |
| `book_table` | Logic | Generates booking reference |
| `save_reservation` | Database | Stores reservation in SQLite |
| `get_reservation` | Database | Retrieves reservation by name |
| `cancel_reservation` | Database | Cancels reservation by reference |
| `get_weather` | API | Gets weather from wttr.in |

## Database Schema

```sql
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT,
    people INTEGER,
    special_requirement TEXT,
    reference INTEGER
)
```

## Booking Flow
```
Customer sends message
↓
Agent checks availability
↓
Agent books table and generates reference
↓
Agent saves reservation to database
↓
Agent confirms with reference number
```

## File Structure
```
**menu.json** — restaurant menu updated without code changes

**faq.txt** — frequently asked questions updated without code changes
```
## Validation Rules

- Session ID cannot be empty
- Message cannot be empty
- Maximum 8 people per table

## Environment Variables
```
API_KEY=your_groq_api_key_here
```

## Notes

- Never commit your .env file to GitHub
- restaurant.db is created automatically on first run
- Session memory resets when server restarts
- Menu and FAQ can be updated without changing code