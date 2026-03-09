import streamlit as st 
from component import event_history,live_alerts,summary

st.title('Police Servillience')

tabs = st.tabs(['Event History', 'Live Alerts', 'Summary'])

with tabs[0]:
    event_history.event_history()

with tabs[1]:
    st.title("Live Alerts")
    st.write("This section will display live alerts from the surveillance system.")
    if st.button('Click me to see live alerts'):
        live_alerts.live_alerts()
    
with tabs[2]:
    summary.show_summary()
    summary.summary()
  