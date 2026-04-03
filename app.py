from flask import Flask, request, jsonify, render_template_string
import sqlite3
from datetime import datetime
from ai_engine import analyze_transaction

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('muthu_mobiles.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            category TEXT,
            amount REAL,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home Page for your husband (Mobile-la azhaga theriyum)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Muthu Mobiles - AI Accountant</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f0f2f5; text-align: center; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        input { width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { background: #007bff; color: white; padding: 12px 20px; border: none; border-radius: 5px; cursor: pointer; width: 95%; font-size: 16px; }
        #status { margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Muthu Mobiles AI</h2>
        <p>Enna transaction-nu type pannunga:</p>
        <input type="text" id="userInput" placeholder="Example: Today swipe 5000 Kumar">
        <button onclick="sendToAI()">Save to Accounts</button>
        <div id="status"></div>
    </div>

    <script>
        async function sendToAI() {
            const text = document.getElementById('userInput').value;
            const status = document.getElementById('status');
            status.innerHTML = "Processing...";
            
            try {
                const response = await fetch('/ask_ai', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                const result = await response.json();
                if(result.status === 'Success') {
                    status.style.color = "green";
                    status.innerHTML = "✅ Saved! " + result.data.category + ": " + result.data.amount;
                    document.getElementById('userInput').value = "";
                } else {
                    status.style.color = "red";
                    status.innerHTML = "❌ Error: " + result.message;
                }
            } catch (e) {
                status.innerHTML = "Connection Error!";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    data = request.json
    user_input = data.get('text')
    
    result = analyze_transaction(user_input)
    
    if result.get('category') != 'Error':
        conn = sqlite3.connect('muthu_mobiles.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (timestamp, category, amount, notes) VALUES (?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), result['category'], result['amount'], result['notes'])
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "Success", "message": "Account-la record aayiduchi!", "data": result})
    else:
        return jsonify({"status": "Error", "message": result['notes']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)