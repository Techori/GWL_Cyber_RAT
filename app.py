from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Terminal se keys hardcode kar rahe hain for stability
LEAK_TOKEN = "7128071523:0Lv2XEkN"
GEMINI_KEY = "AIzaSyAsIUu5qfLvxswYtZp8FTly6BOHYn27KIA"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query: return jsonify({"status": "error", "msg": "Target required"}), 400
    
    url = "https://leakosintapi.com/"
    payload = {"token": LEAK_TOKEN, "request": str(query).strip(), "limit": 100, "lang": "en"}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=25)
        data = response.json()
        results = data.get("List")
        return jsonify({"status": "success", "data": results}) if results else jsonify({"status": "no_data", "msg": "No intelligence found."})
    except:
        return jsonify({"status": "error", "msg": "API Connection Timeout"})

@app.route('/ask_rat', methods=['POST'])
def ask_rat():
    user_data = request.json
    msg = user_data.get('message')
    intel = user_data.get('data', 'No data available')
    
    # Gemini API Call with error handling fix
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": f"You are 'Cyber Rat', a professional intelligence agent. Context: {intel}. User says: {msg}. Respond briefly and professionally."}]}]}
    
    try:
        r = requests.post(api_url, json=payload, timeout=20)
        res = r.json()
        # Path correction for Gemini response
        reply = res['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"reply": "Cyber Rat Neural Link: Signal lost. Checking uplink..."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
