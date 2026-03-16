import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Initialize client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(question, context):

    prompt = f"""
You are an expert software engineer helping developers understand codebases.

Use the provided code context to answer the question.

CODE CONTEXT:
{context}

QUESTION:
{question}

Explain clearly and reference the relevant code if needed.
"""

    response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt
)

    return response.text