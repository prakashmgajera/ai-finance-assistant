import streamlit as st

def get_session_state():
    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = []
    return st.session_state['conversation']
