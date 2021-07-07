from pydoc import text
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import requests
from playsound import playsound
import simpleaudio as sa
import vlc
from pydub import AudioSegment
from pydub.playback import play
import urllib
import pyaudio
import wave

def nghe():  
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return WAVE_OUTPUT_FILENAME
def hieu(path):
    url = 'https://api.fpt.ai/hmi/asr/general'
    payload = open(path, 'rb').read()
    headers = {
        'api-key': 'L8ZnWxr0xSB5IP2h256evRwYPiAFDWoh'
    }

    response = requests.post(url=url, data=payload, headers=headers)

    print(response.json()['hypotheses'][0]['utterance'])
    print(response.json())
    return response.json()['hypotheses'][0]['utterance']
def xuli(text_khach):
    url='http://0.0.0.0:9999/getreponse'
    dataload={
    "msg": text_khach
    }
    
    intent=requests.post(url=url,json=dataload)
    print(intent.json()['intent'])
    return intent.json()['intent']
def noi(text_bot):
    url = 'https://api.fpt.ai/hmi/tts/v5'

    payload = text_bot
    headers = {
        'api-key': 'L8ZnWxr0xSB5IP2h256evRwYPiAFDWoh',
        'speed': '',
        'voice': 'linhsan'
    }

    response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)

    print(response.text)
    print(response.json()['async'])
    
    filename = "say.mp3"
    # Download an mp3 file
    print("downloading mp3 file....")
    urllib.request.urlretrieve(response.json()['async'], filename)
    # load the file into pydub
    birdsound = AudioSegment.from_mp3(filename)
    print("Playing mp3 file...")
    # Play the result
    play(birdsound)
    print("Finished.")
path_nghe=nghe()
text_khach=hieu(path_nghe)
text_bot=xuli(text_khach)
noi(text_bot)
