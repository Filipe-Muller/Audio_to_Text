import pyaudio
import websockets
import asyncio
import base64
import json


AUTH_KEY = '<API_KEY>'
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
PACE_THRESHOLD_FAST = 160
PACE_THRESHOLD_SLOW = 120

p = pyaudio.PyAudio()

# Inicia a gravação
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


async def send_receive():
    print(f'Connecting websocket to url {URL}')
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", AUTH_KEY),),
        ping_interval=5,
        ping_timeout=20
    ) as _ws:
        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")
        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                await asyncio.sleep(0.01)

            return True

        async def receive():
            while True:
                try:
                    result_str = await _ws.recv()
                    print(json.loads(result_str)['text'])
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())

        # Verificação da taxa de fala do palestrante (em tempo real)
        initial_audio = int(json.loads(result_str)['audio_start'])
        end_audio = int(json.loads(result_str)['audio_end'])
        total_audio_time = end_audio - initial_audio
        audio_in_minutes = total_audio_time / 60000  # Conversão de tempo de ms para minutos
        words = json.loads(result_str)['text']
        count_words = words.split()
        total_words = len(count_words)
        pace = total_words / audio_in_minutes

        match pace:
            case _ if pace > PACE_THRESHOLD_FAST:
                print("\nThe speaker's speaking rate is too fast!\n")
            case _ if pace < PACE_THRESHOLD_SLOW:
                print("\nThe speaker's speaking rate is too slow!\n")
            case _:
                print("\nThe speaker's speaking rate is OK!\n")


asyncio.run(send_receive())
