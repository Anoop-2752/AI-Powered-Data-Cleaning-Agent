import streamlit as st
import pandas as pd
import os
from main import run_data_cleaning
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_groq_suggestions(report_text):
    """
    Get AI-powered cleaning suggestions from Groq API
    """
    try:
        completion = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a data cleaning expert."},
                {"role": "user", "content": f"Here is my data cleaning report:\n{report_text}\n\nSuggest improvements or next steps."}
            ],
            temperature=0.7
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        return f"⚠️ Error fetching Groq suggestions: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="Data Cleaning Agent", layout="wide")
st.title("🧹 Data Cleaning Agent with AI Suggestions")

mode = st.radio(
    "Choose mode:",
    ("Run Full Cleaning + AI Suggestions", "Only AI Suggestions (Skip Cleaning)"),
    horizontal=True
)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    if mode == "Run Full Cleaning + AI Suggestions":
        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Run cleaning pipeline
        with st.spinner("Cleaning data..."):
            df_clean, report_text, processed_path = run_data_cleaning(temp_path)

        st.subheader("📊 Cleaned Data Preview")
        st.dataframe(df_clean.head())

        st.subheader("📝 Data Cleaning Report")
        st.text(report_text)

        # Get AI suggestions from Groq
        with st.spinner("Getting AI suggestions..."):
            groq_suggestions = get_groq_suggestions(report_text)

        st.subheader("🤖 Groq AI Suggestions")
        st.write(groq_suggestions)

        # Download buttons
        st.download_button("⬇️ Download Cleaned CSV", df_clean.to_csv(index=False), "cleaned_data.csv", "text/csv")
        st.download_button("⬇️ Download Report", report_text, "data_cleaning_report.txt", "text/plain")

    else:  # Only AI Suggestions mode
        st.info("Upload a report file (.txt) from a previous cleaning run.")
        report_file = st.file_uploader("Upload Report", type=["txt"], key="report_file")

        if report_file is not None:
            report_text = report_file.read().decode("utf-8")

            st.subheader("📝 Loaded Data Cleaning Report")
            st.text(report_text)

            with st.spinner("Getting AI suggestions..."):
                groq_suggestions = get_groq_suggestions(report_text)

            st.subheader("🤖 Groq AI Suggestions")
            st.write(groq_suggestions)
