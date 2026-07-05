import google.generativeai as genai
from backend.config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(question: str):
    """
    Sends a well-engineered educational prompt to Gemini.
    """

    prompt = f"""
You are EduGenie, an AI Powered Educational Assistant.

Your job is to teach students in a simple, accurate, and beginner-friendly way.

Instructions:
- Explain concepts clearly.
- Use simple English.
- Use headings.
- Use bullet points whenever possible.
- Give one real-life example.
- If applicable, provide a small code example.
- End with one important takeaway.

Student Question:
{question}
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"