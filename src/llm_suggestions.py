# src/llm_suggestions.py

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_llm_suggestions(cleaning_summary: str, validation_summary: str) -> list:
    """
    Send cleaning & validation summaries to Groq LLaMA-3 for AI cleaning suggestions.
    """
    prompt = f"""
    You are a data cleaning assistant.
    Based on the cleaning and validation summaries below, give concise, actionable suggestions 
    to further improve the dataset quality.

    Cleaning Summary:
    {cleaning_summary}

    Validation Summary:
    {validation_summary}

    Output each suggestion as a short bullet point.
    """

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Free & very capable
            messages=[
                {"role": "system", "content": "You are a helpful data cleaning assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )

        suggestions_text = response.choices[0].message.content.strip()
        return [s.strip(" -") for s in suggestions_text.split("\n") if s.strip()]

    except Exception as e:
        print(f"⚠️ Groq API error: {e}")
        return []
