import streamlit as st
from api_client import get_events
import time

# async def live_alerts():
#     # st.title("Live Alerts")
#     # st.write("This section will display live alerts from the surveillance system.")
#     placeholder = st.empty()
#     for _ in range(5):
    
#         events = get_events()
#         recent = events[-5:]
#         placeholder.table([
#             {
#                 'timestamp': r.get("timestamp"),
#                 'event type':r.get("event_type"),
#                 'id':r.get("id"),
#                 'zone':r.get("zone"),
#             }
#             for r in recent
#         ])

import streamlit as st
from api_client import get_events

def live_alerts():
    placeholder = st.empty()

    events = get_events()
    recent = events[-5:]

    placeholder.table([
        {
            "timestamp": r.get("timestamp"),
            "event_type": r.get("event_type"),
            "id": r.get("id"),
            "zone": r.get("zone"),
        }
        for r in recent
    ])

# if st.button('Click me to see live alerts'):
#     live_alerts()

    