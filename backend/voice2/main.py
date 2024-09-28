import time
import sounddevice as sd
from audio_recording import audio_callback, save_recording
from tts_utils import speak
import DF_BOT_SUM2 as bot_module
from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import re

app = Flask(__name__)
CORS(app)

fs = 44100
duration = 200
threshold = 50
block_duration = 0.1
max_silent_blocks = 20
recording = [False]
start_time = time.time()
recorded_frames = []
silent_blocks = [0]
stop_stream = [False]

def run_audio_stream():
    try:
        with sd.InputStream(callback=lambda indata, frames, time, status: audio_callback(indata, frames, time, status, threshold, silent_blocks, max_silent_blocks, recording, recorded_frames, start_time, speak, stop_stream), channels=2, samplerate=fs, blocksize=int(fs * block_duration)):
            while not stop_stream[0]:
                sd.sleep(100)
    except Exception as e:
        print(f"오류 발생: {e}")

def run_bot(db_config):
    bot = bot_module.Bot(r"C:\Users\user\Desktop\stunnerkiosk\backend\voice2\my-project-1004-413005-c6a404a02fd6.json", 'cjsrhkdgus1.mp3', db_config)
    bot.load_audio()
    bot.recognize_speech()
    bot.preprocess_text()
    if bot.transcript is None:
        return False
    response = bot.detect_intent_texts('my-project-1004-413005', 'fixed_session_id', 'ko')
    bot.save_parameters_to_db(response)
    if bot.check_parameters_to_db(response):
        return True
    bot.close_db_connection()
    return False

def reset_stream_status():
    global stop_stream, recording, recorded_frames, silent_blocks, start_time
    stop_stream[0] = False
    recording[0] = False
    recorded_frames.clear()
    silent_blocks[0] = 0
    start_time = time.time()

def main_loop(db_config):
    while True:
        run_audio_stream()
        if run_bot(db_config):
            break
        reset_stream_status()
        time.sleep(1)

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language="ko-KR")
        print(f"Recognized text: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio")
        return ""
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
        return ""

def parse_order_text(text):
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

@app.route('/recognize', methods=['POST'])
def recognize():
    recognized_text = recognize_speech_from_mic()
    order = parse_order_text(recognized_text)
    return jsonify(order)

if __name__ == "__main__":
    db_config = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'tlswo3850',
        'host': 'localhost',
        'port': 5432,
    }
    
    # Start the Flask server in a separate thread
    from threading import Thread
    server_thread = Thread(target=lambda: app.run(port=5001, use_reloader=False))
    server_thread.start()
    
    # Start the main loop
    main_loop(db_config)
