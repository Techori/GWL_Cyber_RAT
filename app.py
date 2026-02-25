from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Keys integrated via terminal (No Dashboard required)
LEAK_TOKEN = "7128071523:0Lv2XEkN"
GEMINI_KEY = "AIzaSyAsIUu5qfLvxswYtZp8FTly6BOHYn27KIA"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return jsonify({"status": "error", "msg": "Target required"}), 400
    
    url = "https://leakosintapi.com/"
    payload = {"token": LEAK_TOKEN, "request": str(query).strip(), "limit": 100, "lang": "en"}
    headers = {'Content-Type': 'application/json'}
    
    try:
        # Timeout ko badha kar 30 seconds kiya taaki connection break na ho
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # API response key check karein
            results = data.get("List") or data.get("Data")
            if results:
                return jsonify({"status": "success", "data": results})
            return jsonify({"status": "no_data", "msg": "Intelligence grid empty for this target."})
        return jsonify({"status": "api_error", "msg": f"API Rejected: {response.status_code}"})
    
    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "msg": "Connection Timeout: API is taking too long."})
    except Exception as e:
        return jsonify({"status": "crash", "msg": str(e)})

@app.route('/ask_rat', methods=['POST'])
def ask_rat():
    user_msg = request.json.get('message')
    osint_data = request.json.get('data', 'No data found.')
    
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    prompt = f"You are 'Cyber Rat', a professional OSINT AI. Analyze this OSINT data: {osint_data}. User asks: {user_msg}. Respond like a hacker agent."
    
    try:
        res = requests.post(gemini_url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20).json()
        reply = res['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "Cyber Rat Neural Link: Signal lost."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
