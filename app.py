import streamlit as st

# Debugging: Print all secrets
st.write("Secrets:", st.secrets)

# Load credentials from Streamlit secrets
try:
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(st.secrets["CREDENTIALS_JSON"])
    )
    st.success("Credentials loaded successfully!")
except KeyError:
    st.error("CREDENTIALS_JSON not found in Streamlit secrets. Please add it to secrets.toml or the app settings.")
    st.stop()
