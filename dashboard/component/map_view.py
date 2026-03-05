# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# from api_client import get_events

# def show_map():
#     st.header("Zone Map")
#     # basic map centered on coordinates
#     m = folium.Map(location=[0, 0], zoom_start=15)
#     events = get_events()
#     for e in events:
#         # placeholder coordinates, replace with your zone mapping logic
#         lat, lon = e.get("lat", 0), e.get("lon", 0)
#         color = {"LOITERING": "blue", "UNATTENDED_OBJECT": "red", "CROWD_SURGE": "orange"}.get(e["event_type"], "gray")
#         folium.CircleMarker([lat, lon], radius=7, color=color, popup=e["event_type"]).add_to(m)
#     st_folium(m, width=700, height=500)