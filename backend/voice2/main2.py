from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import re
import time
import sounddevice as sd
from audio_recording import audio_callback, save_recording
from tts_utils import speak
import DF_BOT_SUM2 as bot_module

# 샘플링 레이트와 녹음 시간 설정
fs = 44100
threshold = 50
block_duration = 0.1
max_silent_blocks = 20

# Flask 앱 설정
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # 모든 출처에서의 요청을 허용

# 인식 결과를 캐시하는 변수
cache = {}

# 오디오 스트림 상태 변수
recording = [False]
start_time = time.time()
recorded_frames = []
silent_blocks = [0]
stop_stream = [False]

# 데이터베이스 설정
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'tlswo3850',
    'host': 'localhost',
    'port': 5432,
}

# 봇 객체 생성
bot = bot_module.Bot(r"C:\Users\User\Desktop\졸작\Stunner-kiosk-main\voisk\backend\voice\my-project-1004-413005-c6a404a02fd6.json", 'cjsrhkdgus1.mp3', db_config)

def run_audio_stream():
    try:
        with sd.InputStream(callback=lambda indata, frames, time, status: audio_callback(indata, frames, time, status, threshold, silent_blocks, max_silent_blocks, recording, recorded_frames, start_time, speak, stop_stream), channels=2, samplerate=fs, blocksize=int(fs * block_duration)):
            while not stop_stream[0]:
                sd.sleep(100)  # 짧은 주기로 스트림 상태를 감시
    except Exception as e:
        print(f"오류 발생: {e}")

def run_bot():
    bot.load_audio()
    bot.recognize_speech()
    bot.preprocess_text()
    response = bot.detect_intent_texts('my-project-1004-413005', 'fixed_session_id', 'ko')
    bot.save_parameters_to_db(response)
    return response

def parse_order_text(text):
    if not isinstance(text, str):
        raise ValueError("Expected a string input for parse_order_text")

    add_pattern = r"더블 불고기 버거 (\d+)개 추가해줘"
    new_order_pattern = r"더블 불고기 버거 (\d+)개 담아줘"
    
    add_match = re.search(add_pattern, text)
    new_order_match = re.search(new_order_pattern, text)
    
    if add_match:
        count = int(add_match.group(1))
        return {"item": "더블 불고기 버거", "count": count, "type": "add"}
    elif new_order_match:
        count = int(new_order_match.group(1))
        return {"item": "더블 불고기 버거", "count": count, "type": "new"}
    else:
        return {"item": "더블 불고기 버거", "count": 1, "type": "new"}

@app.route('/process_audio', methods=['POST'])
def process_audio():
    data = request.json
    speech_text = data.get('speech', '')
    
    # Run bot to process the speech
    bot.transcript = speech_text
    response = run_bot()
    
    recognized_text = response.query_result.fulfillment_text
    order = parse_order_text(recognized_text)
    
    return jsonify(order)

if __name__ == "__main__":
    app.run(port=5001)