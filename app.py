from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from ai_engine import analyze_transaction

app = Flask(__name__)
CORS(app)

def save_to_db(category, amount, notes):
    conn = sqlite3.connect('muthu_mobiles.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transactions (category, amount, notes) VALUES (?, ?, ?)', (category, amount, notes))
    conn.commit()
    conn.close()

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    user_text = request.json.get('text')
    ai_data = analyze_transaction(user_text)
    save_to_db(ai_data['category'], ai_data['amount'], ai_data['notes'])
    return jsonify({'status': 'Success', 'message': 'Account-la record aayiduchi!', 'data': ai_data})

if __name__ == '__main__':
    print('AI Accountant is live on port 5000...')
    app.run(debug=True, port=5000)
