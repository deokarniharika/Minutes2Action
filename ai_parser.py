import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Initialize model
model = genai.GenerativeModel("gemini-2.5-flash")


def extract_tasks(transcript):

    prompt = f"""
You are an AI project manager.

Extract action items from the meeting transcript.

Return ONLY valid JSON.
Do not include explanations or markdown.

Use this format:

{{
 "tasks":[
  {{
   "task":"",
   "owner":"",
   "deadline":""
  }}
 ]
}}

Meeting Transcript:
{transcript}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Clean response in case the model adds extra text
    start = text.find("{")
    end = text.rfind("}") + 1

    if start != -1 and end != -1:
        clean_json = text[start:end]
        return clean_json

    return '{"tasks":[]}'