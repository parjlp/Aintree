import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

df_1245 = pd.read_csv("1245.csv", encoding="latin-1")
df_1245 = df_1245["Name"].tolist()
df_1320 = pd.read_csv("1320.csv", encoding="latin-1")
df_1320 = df_1320["Name"].tolist()
df_1355 = pd.read_csv("1355.csv", encoding="latin-1")
df_1355 = df_1355["Name"].tolist()
df_1430 = pd.read_csv("1430.csv", encoding="latin-1")
df_1430 = df_1430["Name"].tolist()
df_1505 = pd.read_csv("1505.csv", encoding="latin-1")
df_1505 = df_1505["Name"].tolist()
df_1600 = pd.read_csv("1600.csv", encoding="latin-1")
df_1600 = df_1600["Name"].tolist()
df_fgs = pd.read_csv("fgs.csv", encoding="latin-1")
df_fgs = df_fgs["Player"].tolist()

def get_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(creds)
    return client.open("1vBWWgRsrN1VD1MfdKatQz3uGfWWU_BKotM742cb3o2s").sheet1


def submit_details():
    if not st.session_state["name"].strip():
        return

    picks = {
        "Name": st.session_state["name"],
        "12:45": st.session_state["12:45"],
        "13:20": st.session_state["13:20"],
        "13:55": st.session_state["13:55"],
        "14:30": st.session_state["14:30"],
        "15:05": st.session_state["15:05"],
        "16:00": st.session_state["16:00"],
        "FGS":   st.session_state["FSG"],
    }

    sheet = get_sheet()
    sheet.append_row(list(picks.values()))

    send_email(picks)

st.title("Enter Your Selections For Grand National Day 2026")
st.divider()

with st.form("Aintree Submit"):
    name = st.text_input(key="name", label="Please enter your full name")
    st.divider()
    pick_1245 = st.selectbox(key="12:45", options=df_1245, label="12:45 Maghull Novice's Chase (Grade 1)")
    st.divider()
    pick_1320 = st.selectbox(key="13:20", options=df_1320, label="13:20 Handicap Hurdle (Class 1)")
    st.divider()
    pick_1355 = st.selectbox(key="13:55", options=df_1355, label="13:55 Mersey Novice's Hurdle (Grade 1)")
    st.divider()
    pick_1430 = st.selectbox(key="14:30", options=df_1430, label="14:30 Handicap Chase (Class 1)")
    st.divider()
    pick_1505 = st.selectbox(key="15:05", options=df_1505, label="15:05 Liverpool Hurdle (Grade 1)")
    st.divider()
    pick_1600 = st.selectbox(key="16:00", options=df_1600, label="16:00 Grand National Handicap Chase (Class 1)")
    st.divider()
    pick_fgs = st.selectbox(key="FSG", options=df_fgs, label="Liverpool vs Fulham First Goal Scorer")
    st.divider()
    submitted = st.form_submit_button("Submit", on_click=submit_details)
    if submitted:
        if st.session_state["name"].strip():
            st.success("Submitted successfully!")
        else:
            st.warning("Please enter your full name before submitting.")
