from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import DF_BOT_SUM2 as bot_module

# Flask 앱 설정
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 데이터베이스 설정
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'tlswo3850',
    'host': 'localhost',
    'port': 5432,
}

# 봇 객체 생성
bot = bot_module.Bot(
    r"C:\Users\User\Desktop\졸작\Stunner-kiosk-main\voisk\backend\voice\my-project-1004-413005-c6a404a02fd6.json", 
    'cjsrhkdgus1.mp3', 
    db_config
)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    data = request.json
    speech_text = data.get('speech', '')

    if speech_text:
        bot.transcript = speech_text
        bot.recognize_speech(speech_text)
        bot.preprocess_text()
        response = bot.detect_intent_texts('my-project-1004-413005', 'fixed_session_id', 'ko')
        bot.save_parameters_to_db(response)

        recognized_text = response.query_result.fulfillment_text

        # 주문 처리 로직 추가
        if "담아줘" in recognized_text:
            item = "불고기 버거"  # 이 부분은 더 복잡한 로직으로 대체할 수 있습니다.
            order_response = requests.post('http://localhost:8000/order', json={"message": item})
            if order_response.status_code != 200:
                return jsonify({"error": "Failed to process order"}), 500

        return jsonify({"recognized_text": recognized_text})

    return jsonify({"error": "No speech text provided"}), 400

if __name__ == "__main__":
    app.run(port=5001)
