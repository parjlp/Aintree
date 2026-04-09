import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Connect to Google Sheets
def get_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(creds)
    return client.open("Aintree Selections").sheet1

def submit_details():
    if not st.session_state["name"].strip():
        return

    sheet = get_sheet()
    sheet.append_row([
        st.session_state["name"],
        st.session_state["12:45"],
        st.session_state["13:20"],
        st.session_state["13:55"],
        st.session_state["14:30"],
        st.session_state["15:05"],
        st.session_state["16:00"],
        st.session_state["FSG"],
    ])
