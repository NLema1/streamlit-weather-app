import streamlit as st
import json
import os
from google.cloud import bigquery

# Step 1: Load Google Cloud credentials from Streamlit Secrets
try:
    gcp_credentials = json.loads(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])
    st.success("✅ Google Cloud credentials loaded successfully.")
except Exception as e:
    st.error(f"❌ Failed to load Google Cloud credentials: {e}")
    st.stop()

# Step 2: Write credentials to a temporary JSON file
with open("/tmp/gcp_credentials.json", "w") as f:
    json.dump(gcp_credentials, f)

# Step 3: Set the environment variable to point to the credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/gcp_credentials.json"

# Step 4: Initialize BigQuery client
try:
    bq_client = bigquery.Client()
    st.success("✅ BigQuery client initialized successfully.")
except Exception as e:
    st.error(f"❌ Failed to initialize BigQuery client: {e}")
    st.stop()

# Step 5: Sample query to BigQuery
def fetch_data():
    query = """
    SELECT timestamp, temperature_category, overall_grade
    FROM `jumpfree.weather_dataset.weather_data`
    LIMIT 10
    """
    query_job = bq_client.query(query)
    return query_job.to_dataframe()

# Step 6: Streamlit App UI
st.title("🪂 Skydiving Weather Dashboard")
st.write("Fetching data from BigQuery...")

# Fetch and display data
try:
    df = fetch_data()
    st.write(df)
except Exception as e:
    st.error(f"❌ Error fetching data: {e}")
