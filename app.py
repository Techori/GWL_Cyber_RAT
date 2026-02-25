from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
LEAK_TOKEN = os.environ.get('LEAKOSINT_TOKEN', '7128071523:0Lv2XEkN')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return jsonify({"status": "error", "msg": "Input required"}), 400
    
    url = "https://leakosintapi.com/"
    # Payload as a Python Dict
    payload = {
        "token": LEAK_TOKEN, 
        "request": str(query).strip(), 
        "limit": 100, 
        "lang": "en"
    }
    
    try:
        # Strict JSON Headers add kiye hain
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        # json=payload ensures formatting is correct JSON
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("List")
            if results:
                return jsonify({"status": "success", "data": results})
            else:
                return jsonify({"status": "no_data", "msg": "Target not found in intelligence grid"})
        else:
            return jsonify({"status": "api_error", "msg": f"Server Refused Request (Code: {response.status_code})"})
            
    except Exception as e:
        return jsonify({"status": "crash", "msg": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
