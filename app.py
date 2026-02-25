from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Environment variables from Render
LEAK_TOKEN = os.environ.get('LEAKOSINT_TOKEN', '7128071523:0Lv2XEkN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return jsonify({"status": "error", "msg": "Target required"}), 400
    
    url = "https://leakosintapi.com/"
    # Strict JSON formatting
    payload = {"token": LEAK_TOKEN, "request": str(query).strip(), "limit": 100, "lang": "en"}
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        data = response.json()
        results = data.get("List")
        if results:
            return jsonify({"status": "success", "data": results})
        return jsonify({"status": "no_data", "msg": "No response: Intelligence grid empty."})
    except Exception as e:
        return jsonify({"status": "crash", "msg": str(e)})

@app.route('/ask_rat', methods=['POST'])
def ask_rat():
    user_msg = request.json.get('message')
    osint_data = request.json.get('data', 'No data found.')
    
    if not GEMINI_KEY:
        return jsonify({"reply": "Cyber Rat logic offline: Missing Neural Key."})

    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    prompt = f"You are 'Cyber Rat', a professional OSINT AI. Analyze this data: {osint_data}. User asks: {user_msg}. Respond like a hacker agent."
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(gemini_url, json=payload).json()
        reply = res['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "Connection lost to Cyber Rat Core."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
