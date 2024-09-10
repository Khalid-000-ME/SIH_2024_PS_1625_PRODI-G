from flask import Flask, jsonify
import json
from flask_cors import CORS
from modules import gemini

app = Flask(__name__)
CORS(app)

@app.route('/chatbot/<prompt>')
def chatbot(prompt):
    return gemini.chatbot(prompt)

p = "modules/files/note.txt"

@app.route('/quiz')
def quiz():
    return gemini.quiz(p)

if __name__ == "__main__":
    app.run(debug=True)