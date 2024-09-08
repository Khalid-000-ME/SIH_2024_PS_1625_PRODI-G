from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/run-python-script')
def run_python_script():
    print("\nRoute accessed\n")
    result = subprocess.run(['python', r'E:\sih2024\chatbot\learn\script.py'], capture_output=True, text=True)
    return jsonify({'output': result.stdout.strip()})

if __name__ == "__main__":
    with app.test_request_context():
        print([str(rule) for rule in app.url_map.iter_rules()])
    app.run(host='127.0.0.1', port=5000, debug=True)
