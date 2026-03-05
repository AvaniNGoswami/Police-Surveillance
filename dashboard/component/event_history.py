import streamlit as st
from api_client import get_events

def event_history():
    st.title('Event History')
    events = get_events()
    if events:
        st.dataframe(events)
    else:
        st.write('nothing recorded yet')