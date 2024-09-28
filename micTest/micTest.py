import sounddevice as sd
from pydub import AudioSegment
import numpy as np
from scipy.io.wavfile import write

# 녹음 설정
fs = 44100  # 샘플링 주파수
duration = 10  # 녹음할 시간 (초)

# 녹음 시작
print("녹음을 시작합니다.")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()  # 녹음이 끝날 때까지 기다림
print("녹음이 완료되었습니다.")

# 볼륨 증폭 설정
gain = 2.0  # 볼륨을 2배로 증폭
myrecording_amplified = myrecording * gain

# 증폭된 데이터가 -1과 1 사이의 범위에 들어오도록 클리핑
myrecording_amplified = np.clip(myrecording_amplified, -1.0, 1.0)

# 녹음 결과를 wav 파일로 저장
myrecording_amplified = (myrecording_amplified * np.iinfo(np.int16).max).astype(np.int16)
wav_file = 'output_amplified.wav'
write(wav_file, fs, myrecording_amplified)

# wav 파일을 mp3 파일로 변환
audio = AudioSegment.from_wav(wav_file)
audio.export("output_amplified.mp3", format="mp3")
