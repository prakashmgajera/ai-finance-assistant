import streamlit as st

st.set_page_config(page_title="AI Finance Assistant", layout="wide")
st.title("AI Finance Assistant")

st.write("Welcome to the multi-agent financial education assistant.")

# Tabs for Chat, Portfolio, Market, Goals
tabs = st.tabs(["Chat", "Portfolio", "Market", "Goals"])

with tabs[0]:
    st.write("Chat interface coming soon...")
with tabs[1]:
    st.write("Portfolio analysis dashboard coming soon...")
with tabs[2]:
    st.write("Market overview coming soon...")
with tabs[3]:
    st.write("Goal planning coming soon...")
