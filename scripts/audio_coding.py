import requests
import tkinter as tk
from tkinter import simpledialog, messagebox
import logging
import sys

#Only use the command below if your IDE cannot find the repo location in your machine, otherwise you can comment the same
sys.path.append("<REPO_PATH>")
from variables.variables import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_request(url, method="GET", json_data=None):
    headers = {
        "authorization": API_KEY,
        "content-type": "application/json"
    }

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=json_data, headers=headers)
    else:
        raise ValueError(f"Invalid request method: {method}")

    response.raise_for_status()
    return response.json()

def get_audio_transcript(url):
    logger.info(UPLOAD_PROCESSING_MESSAGE)

    json_data = {
        "audio_url": url
    }

    try:
        response = make_request(TRANSCRIPT_ENDPOINT, method="POST", json_data=json_data)
        audio_id = response['id']
        endpoint = f"{TRANSCRIPT_ENDPOINT}/{audio_id}"

        while True:
            response = make_request(endpoint)
            if response['status'] != 'processing':
                break

        return response
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to process the audio transcript. Error: {e}")

def upload_local_file(filename):
    logger.info(UPLOAD_PROCESSING_MESSAGE)

    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    response_upload = make_request(UPLOAD_ENDPOINT, method="POST", json_data=None)
    endpoint_upload = response_upload['upload_url']

    json_data = {"audio_url": endpoint_upload}
    response = make_request(TRANSCRIPT_ENDPOINT, method="POST", json_data=json_data)

    audio_id = response['id']
    endpoint = f"{TRANSCRIPT_ENDPOINT}/{audio_id}"

    while True:
        response = make_request(endpoint)
        if response['status'] != 'processing':
            break

    return response

def check_speaking_rate(response):
    if 'audio_duration' not in response or 'text' not in response:
        raise ValueError(FILE_EXTRACTION_FAILED)

    audio_duration = response.get('audio_duration')
    if audio_duration is not None:
        audio_duration = int(audio_duration)
    else:
        raise ValueError("Audio duration not available in the response.")

    words = response['text']
    count_words = len(words.split())
    pace = count_words / audio_duration * 60

    message = f"Pace: {pace:.2f} words per minute\n\n"

    if pace > SPEAKING_RATE_THRESHOLD_FAST:
        message += f"🏃‍♂️ {SPEAKING_RATE_FAST_MESSAGE}"
    elif pace < SPEAKING_RATE_THRESHOLD_SLOW:
        message += f"🐢 {SPEAKING_RATE_SLOW_MESSAGE}"
    else:
        message += f"👌 {SPEAKING_RATE_ACCEPTABLE_MESSAGE}"

    messagebox.showinfo("Result", message)

def get_user_input():

    def on_upload_url():
        root.destroy()
        url = simpledialog.askstring("Input", URL_PROMPT)
        try:
            response = get_audio_transcript(url)
            check_speaking_rate(response)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def on_upload_local_file():
        root.destroy()
        filename = simpledialog.askstring("Input", FILENAME_PROMPT)
        try:
            response = upload_local_file(filename)
            check_speaking_rate(response)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def on_closing():
        root.destroy()

    root = tk.Tk()
    root.title(APP_LABEL)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    instruction_label = tk.Label(root, text=APP_LABEL, padx=10, pady=10)
    instruction_label.pack()

    upload_url_button = tk.Button(root, text=URL_OPTION, command=on_upload_url)
    upload_url_button.pack(pady=5)

    upload_local_file_button = tk.Button(root, text=FILE_OPTION, command=on_upload_local_file)
    upload_local_file_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    get_user_input()
