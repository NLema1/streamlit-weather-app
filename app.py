import streamlit as st
import pandas as pd
from google.cloud import bigquery
import matplotlib.pyplot as plt

# Access the secret
gcp_credentials = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]

# Set the environment variable for Google Cloud authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_credentials

# Initialize BigQuery client
bq_client = bigquery.Client()

# Streamlit App Title
st.title("🪂 Skydiving Weather Dashboard")
st.subheader("📊 Real-time Skydiving Weather Conditions")

# Function to fetch data from BigQuery
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def fetch_weather_data():
    query = """
    SELECT 
        timestamp, 
        temperature_category, 
        wind_category, 
        visibility_category, 
        cloud_cover_category, 
        precipitation_category, 
        humidity_category, 
        uv_index_category, 
        overall_grade 
    FROM `jumpfree.weather_dataset.weather_data`
    ORDER BY timestamp DESC
    LIMIT 100
    """
    query_job = bq_client.query(query)
    df = query_job.to_dataframe()
    return df

# Load data
data = fetch_weather_data()

# Show data table
st.dataframe(data)

# Plot overall grades over time
st.subheader("📈 Overall Skydiving Conditions Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.sort_values('timestamp', inplace=True)
ax.plot(data['timestamp'], data['overall_grade'], marker='o', linestyle='-')
ax.set_xlabel("Timestamp")
ax.set_ylabel("Skydiving Grade")
plt.xticks(rotation=45)
st.pyplot(fig)

# Show latest skydiving grade
if not data.empty:
    latest_grade = data.iloc[0]['overall_grade']
    st.markdown(f"### 🟢 Latest Skydiving Grade: **{latest_grade}**")
else:
    st.warning("No data available.")
