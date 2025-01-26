import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
from google.oauth2 import service_account

# Load credentials from Streamlit secrets
try:
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(st.secrets["CREDENTIALS_JSON"]),
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    st.success("Credentials loaded successfully!")
except KeyError:
    st.error("CREDENTIALS_JSON not found in Streamlit secrets. Please add it to secrets.toml or the app settings.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading credentials: {e}")
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

# Main Function
def main():
    st.title("Google Sheets Data Viewer 📊")

    # URL of your Google Sheet
    sheet_url = st.text_input("Enter the Google Sheet URL:", "https://docs.google.com/spreadsheets/d/1Gx3MO9HMlquaV2fh3w4LqF-gGbbPnkTh7-vEpB-LPvU/edit?resourcekey=&gid=2000238640#gid=2000238640")

    # Button to fetch and display data
    if st.button("Fetch Data"):
        # Authenticate and fetch data
        data = authenticate_google_sheets(sheet_url)

        if data:
            st.success("Data fetched successfully!")
            # Convert data to a pandas DataFrame for better display
            df = pd.DataFrame(data)

            # Display the data in an interactive table
            st.write("### Raw Data")
            st.dataframe(df)

            # Add filters
            st.sidebar.header("Filters")
            filter_column = st.sidebar.selectbox("Filter by Column", df.columns)
            filter_value = st.sidebar.text_input(f"Enter value for {filter_column}")

            if filter_value:
                filtered_df = df[df[filter_column].astype(str).str.contains(filter_value, case=False)]
                st.write(f"### Filtered Data (where {filter_column} contains '{filter_value}')")
                st.dataframe(filtered_df)
            else:
                st.write("### No filters applied")

            # Add sorting
            st.sidebar.header("Sorting")
            sort_column = st.sidebar.selectbox("Sort by Column", df.columns)
            sort_order = st.sidebar.radio("Sort Order", ["Ascending", "Descending"])

            if sort_column:
                if sort_order == "Ascending":
                    sorted_df = df.sort_values(by=sort_column, ascending=True)
                else:
                    sorted_df = df.sort_values(by=sort_column, ascending=False)
                st.write(f"### Sorted Data (by {sort_column}, {sort_order})")
                st.dataframe(sorted_df)
        else:
            st.error("Failed to fetch data from Google Sheets.")

# Run the app
if __name__ == "__main__":
    main()
