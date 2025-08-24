import os
import google.generativeai as genai
import json
from app.config import settings

try:
    genai.configure(api_key=settings.AI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    print(f"Error configuring AI model: {e}")
    model = None

def get_ai_analysis(job_text: str) -> dict:
    if not model:
        return {"error": "AI model is not configured."}

    prompt = f"""
    You are an expert career coach and HR analyst. Your task is to analyze the following job description and extract key information.

    Analyze the text below and return a JSON object with three specific keys: "summary", "requirements", and "action_plan".

    1.  **summary**: A concise, professional summary of the job role in 2-3 sentences.
    2.  **requirements**: An array of strings, listing the 5-7 most critical skills, technologies, or experience qualifications.
    3.  **action_plan**: An array of strings, providing 3-5 concrete, actionable steps a candidate could take to meet the requirements.

    Job Description:
    ---
    {job_text}
    ---

    Return ONLY the JSON object, with no other text, explanations, or markdown formatting.
    """

    try:
        response = model.generate_content(prompt)

        cleaned_text = response.text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3] 
        
        return json.loads(cleaned_text)
    
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from AI response: {response.text}")
        return {"error": "AI returned a malformed response."}
    
    except Exception as e:
        print(f"An error occurred during AI analysis: {e}")
        return {"error": "Failed to parse AI response."}