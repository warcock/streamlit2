import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
from google.oauth2 import service_account

# Load credentials from Streamlit secrets
try:
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(st.secrets["CREDENTIALS_JSON"])
    )
except KeyError:
    st.error("CREDENTIALS_JSON not found in Streamlit secrets. Please add it to secrets.toml or the app settings.")
    st.stop()

# Step 1: Authenticate and Access Google Sheets
def authenticate_google_sheets(sheet_url):
    try:
        # Define the scope
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

        # Use the credentials loaded from secrets
        client = gspread.authorize(credentials)

        # Open the Google Sheet by URL
        sheet = client.open_by_url(sheet_url).sheet1  # Use the first sheet

        # Fetch all data
        expected_headers = ["Nickname", "Instagram Username"]
        data = sheet.get_all_records(expected_headers=expected_headers)
        return data
    except Exception as e:
        st.error(f"An error occurred while fetching data from Google Sheets: {e}")
        return None
