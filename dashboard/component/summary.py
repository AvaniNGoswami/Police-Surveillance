import streamlit as st 
from api_client import get_hour_summary,get_summary

# def summary():
#     hour_summary = get_hour_summary()
#     if hour_summary:
#         st.json(hour_summary)
#     else:
#         st.write('Summary unavailable')

# def show_summary():
#     st.header("Hourly Summary")

#     data = get_hour_summary()

#     if not data:
#         st.write("Summary unavailable.")
#         return

#     st.text(data.get("summary", "No summary available."))

def show_summary():
    st.header("Hourly Summary")

    data = get_hour_summary()

    if not data:
        st.write("Summary unavailable.")
        return

    st.text(data.get("summary"))

    if data.get("data"):
        st.table(data["data"])



def summary():
    data = get_summary()
    if not data:
        st.write("Summary unavailable.")
        return

    st.text(data.get("summary"))

    if data.get("data"):
        st.table(data["data"])
