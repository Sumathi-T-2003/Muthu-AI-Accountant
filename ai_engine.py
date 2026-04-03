import google.generativeai as genai
import json
import re

genai.configure(api_key='AIzaSyDLNVhGMl3JL8347T1f3iRfilOJd9aQLoc')
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

def analyze_transaction(user_input):
    prompt = f'Extract business data from: {user_input}. Return ONLY JSON: {{"category": "Swipe", "amount": 5000, "notes": "notes"}}'
    try:
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group(0)) if match else json.loads(response.text.strip())
    except Exception as e:
        return {'category': 'Error', 'amount': 0, 'notes': str(e)}
