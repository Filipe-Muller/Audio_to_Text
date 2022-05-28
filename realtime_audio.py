import pyaudio
import websockets
import asyncio
import base64
import json

auth_key = 'a47eb48ba4194ef0b0c875c21a41e1bd'

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

# starts recording
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


async def send_receive():
    print(f'Connecting websocket to url ${URL}')
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", auth_key),),
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

        # Speaker's speaking rate check (real time)
        initial_audio = (int(json.loads()['audio_start']))
        end_audio = (int(json.loads()['audio_end']))
        total_audio_time = end_audio - initial_audio
        audio_in_minutes = total_audio_time/60000  # time conversion -> ms to min
        words = json.loads()['text']
        count_words = words.split()
        total_words = int(len(count_words))
        pace = total_words/audio_in_minutes

        if(pace > 160):
            print("\nThe speaker's speaking rate is too fast!\n")

        elif(pace < 120):
            print("\nThe speaker's speaking rate is too slow!\n")

        else:
            print("\nThe speaker's speaking rate is OK!\n")

asyncio.run(send_receive())
