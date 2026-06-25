from flask import Flask, render_template, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)

# 🔑 นำ Client ID ของจริงที่คุณสร้างจาก Google Cloud Console มาวางตรงนี้ครับ
CLIENT_ID = "969552580845-v4tu5aibk6m9sb3fieu0dtrmc0cvm3aj.apps.googleusercontent.com"

@app.route('/')
def index():
    # ฟังก์ชันนี้จะทำหน้าที่ส่งหน้า HTML ไปแสดงผล และเปลี่ยน {{ client_id }} ให้เป็นรหัสจริงอัตโนมัติ
    return render_template('index.html', client_id=CLIENT_ID)

@app.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.json.get('credential')
    try:
        # ตรวจสอบความถูกต้องของ Token กับเซิร์ฟเวอร์ Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        
        return jsonify({
            'status': 'success', 
            'user': {
                'name': idinfo.get('name'), 
                'email': idinfo.get('email'), 
                'picture': idinfo.get('picture')
            }
        })
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)