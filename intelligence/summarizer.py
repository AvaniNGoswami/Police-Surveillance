from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from app.db.database import engine
from app.models.event import Event as events

# LLM integration
import os
from groq import Groq

# Ensure GROQ_API_KEY is set in your environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set.")
client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.1-8b-instant"


def call_llm(messages):
    res = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3
    )
    return res.choices[0].message.content

class ShiftSummarizer:
    def __init__(self,vector_store ):
        # self.db_session = db_session
        self.vector_store  = vector_store 

    def fetch_last_hr(self,Event):
        current_time = datetime.utcnow() - timedelta(hours=1)

        with Session(engine) as session:
            last_hour = session.query(events).filter(events.timestamp>=current_time).all()
        return last_hour

    def summary(self):
        recent = self.fetch_last_hr(events)
        if not recent:
            return "No recent events found."
        structured_text = []
        for event in recent:
            text = f'{event.event_type} at zone {event.zone} at {event.timestamp}'
            structured_text.append(text)
            self.vector_store.embed_event(text)
        query_text = " ".join(structured_text)
        similar_past = self.vector_store.search_similar(query_text)
        # Compose a prompt for the LLM
        prompt = f"""
            You are generating a neutral police situational awareness report.

            Output format rules (MANDATORY):
            - Plain text only.
            - No markdown.
            - No bold text.
            - No bullet points.
            - No asterisks.
            - No headings.
            - No symbols such as *, -, #.
            - Use simple paragraphs.
            - Use line breaks only where necessary.
            - Do not structure as sections.
            - Do not add formatting.

            Content rules:
            - Report only facts based on provided data.
            - Include only information supported by the data.
            - Do not speculate.
            - Do not infer intent.
            - Do not accuse individuals.
            - Only describe observable patterns.
            - If one event occurred, state it is isolated.
            - Avoid dramatic language.
            - Focus on statistical patterns and zone frequency.
            """
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query_text}
        ]
        return call_llm(messages)
    
    