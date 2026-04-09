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
    return client.open("Aintree Selections").sheet1

def send_email(picks):
    sender = st.secrets["email"]["sender"]
    password = st.secrets["email"]["password"]
    receiver = st.secrets["email"]["receiver"]

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = f"Aintree Selections - {picks['Name']}"

    body = f"""
    New submission from {picks['Name']}:

    12:45 Maghull Novice's Chase:     {picks['12:45']}
    13:20 Handicap Hurdle:            {picks['13:20']}
    13:55 Mersey Novice's Hurdle:     {picks['13:55']}
    14:30 Handicap Chase:             {picks['14:30']}
    15:05 Liverpool Hurdle:           {picks['15:05']}
    16:00 Grand National:             {picks['16:00']}
    First Goal Scorer:                {picks['FGS']}
    """

    msg.attach(MIMEText(body, "plain"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

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

    # Save to Google Sheets
    sheet = get_sheet()
    sheet.append_row(list(picks.values()))

    # Send email
    send_email(picks)

st.title("Enter Your Selections For Grand National Day 2026")
st.divider()

with st.form("Aintree Submit"):
    name = st.text_input(key="name", label="Please enter your full name")
    st.divider()
    pick_1245 = st.selectbox(key="12:45", options=df_1245, label="12:45 Magh
