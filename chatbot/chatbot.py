import requests
import google.generativeai as genai
import os

API_KEY = 'api_key_here' #API KEY is not mentioned here. Create one in Google AI Studio

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role":"user", "parts":"Hello"},
        {"role":"model", "parts":"Great to meet you. What would you like to know?"}
    ]
)
response = chat.send_message("What is Quantum Entanglement.", generation_config=genai.types.GenerationConfig(
    candidate_count=1,
    stop_sequences=["x"],
    max_output_tokens=150,
    temperature=0.5,
),
)
print(response.text)
response = chat.send_message("Wonderful.")
print(response.text)
