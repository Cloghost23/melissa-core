import os
from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

# Dynamically grab the LLM URL from Docker, fallback to localhost if testing manually
LLAMA_SERVER_URL = os.environ.get("LLAMA_SERVER_URL", "http://127.0.0.1:8080")

# Sliding Window Memory Configuration
chat_history = []
MAX_HISTORY = 10

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    
    # Direct Math Evaluation Bypass Interceptor
    if re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', user_input):
        try:
            result = str(eval(user_input))
            return jsonify({"response": f"Calculated locally: {result}"})
        except Exception:
            pass

    # Update Sliding Memory
    chat_history.append({"role": "user", "content": user_input})
    if len(chat_history) > MAX_HISTORY:
        chat_history.pop(0)

    # Format context and send to llama.cpp inference server
    try:
        payload = {
            "prompt": "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history]) + "\nassistant:",
            "n_predict": 512
        }
        # 120-second timeout patience for mobile hardware spikes
        response = requests.post(f"{LLAMA_SERVER_URL}/completion", json=payload, timeout=120)
        
        if response.status_code == 200:
            ai_text = response.json().get('content', '')
            chat_history.append({"role": "assistant", "content": ai_text.strip()})
            return jsonify({"response": ai_text.strip()})
        else:
            return jsonify({"error": "Inference server error."}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Connection dropped: {str(e)}"}), 500

if __name__ == '__main__':
    # Bind to 0.0.0.0 so Docker can expose the port
    app.run(host='0.0.0.0', port=5000)

