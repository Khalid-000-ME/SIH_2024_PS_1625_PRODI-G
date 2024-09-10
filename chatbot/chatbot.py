from flask import Flask
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyBdzYHCOehJj3fLtboBC1Z57_HFv484ico"

@app.route('/greet/<name>')

def greet(name):
    
    genai.configure(api_key=API_KEY)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(
        history =[
            {'role': 'user', 'parts': 'Hello'},
            {'role': 'model', 'parts': 'Hello, how can I help you with your doubts?'}
        ]
    )
    
    response = chat.send_message(
        name,
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            temperature=0.5,
        ),
    )
    
    return response.text

if __name__ == "__main__":
    app.run(debug=True)
