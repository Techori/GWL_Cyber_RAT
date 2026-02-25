from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Render ke Environment Variables se token lega
LEAK_TOKEN = os.environ.get('LEAKOSINT_TOKEN', 'YOUR_TOKEN_HERE')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return jsonify({"error": "Target input required"})

    # Leakosint API call as per documentation
    url = "https://leakosintapi.com/"
    payload = {
        "token": LEAK_TOKEN, 
        "request": query, 
        "limit": 100, 
        "lang": "en"
    }
    
    try:
        response = requests.post(url, json=payload).json()
        return jsonify(response.get("List", {}))
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
