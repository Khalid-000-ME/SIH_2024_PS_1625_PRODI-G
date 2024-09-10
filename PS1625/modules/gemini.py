import google.generativeai as genai
import json

API_KEY = ""

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat(
        history=[
            {"role":"user", "parts":"Hello"},
            {"role":"model", "parts":"Great to meet you. What would you like to know?"}
        ]
    )

def chatbot(userInput):
    response = chat.send_message(userInput, generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=500,
        temperature=0.5,
    ),)
    
    return response.text

def quiz(path):
    
    f = open(path, 'r+')
    data = f.read()
    f.close()
    prompt = data + "-using the text here, generate five questions in a JSON format, where the i-th question is with the label 'q(i)0' and 4 corresponding multiple choice answers where the j-th answer is with the label 'a(j)' in the JSON format."
    response = chat.send_message(prompt, generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        temperature=0.1,
    ),)
    res = response.text.strip()[7:-3].strip()
    
    return json.loads(res)
