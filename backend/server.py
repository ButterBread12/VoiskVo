from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import re

app = Flask(__name__)
CORS(app)

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
    app.run(port=5001)