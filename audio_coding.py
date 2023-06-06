import requests
from rich import print

#The best approach would be to use the following constants as global ones
API_KEY = "<API_KEY>"
UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"

SPEAKING_RATE_THRESHOLD_FAST = 160
SPEAKING_RATE_THRESHOLD_SLOW = 120

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
    json_data = {
        "audio_url": url
    }
    response = make_request(TRANSCRIPT_ENDPOINT, method="POST", json_data=json_data)

    audio_id = response['id']
    endpoint = f"{TRANSCRIPT_ENDPOINT}/{audio_id}"

    while True:
        response = make_request(endpoint)
        if response['status'] != 'processing':
            break

    return response

def upload_local_file(filename):
    print('\nPlease wait while your audio transcription is being processed...')

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
    audio_duration = int(response['audio_duration'])
    words = response['text']
    count_words = len(words.split())
    pace = count_words / audio_duration * 60

    match pace:
        case _ if pace > SPEAKING_RATE_THRESHOLD_FAST:
            print("\nThe speaker's speaking rate is too fast.")
        case _ if pace < SPEAKING_RATE_THRESHOLD_SLOW:
            print("\nThe speaker's speaking rate is too slow.")
        case _:
            print("\nThe speaker's speaking rate is within the acceptable range.")

def get_user_input(prompt, valid_options):
    while True:
        user_input = input(prompt)
        if user_input in valid_options:
            return user_input
        else:
            print("Invalid input. Please try again.")

def main():
    method = get_user_input(
        "\nType 1 to upload a file via URL or type 2 to upload a local file: ", ["1", "2"]
    )

    if method == '1':
        url = input(
            "\nPlease enter the URL where the desired audio file for transcription is located: "
        )
        response = get_audio_transcript(url)
        check_speaking_rate(response)
    elif method == '2':
        filename = input(
            "\nPlease enter the local file path and name (including the format) of the audio file for transcription: "
        )
        response = upload_local_file(filename)
        check_speaking_rate(response)
    else:
        print("\nInvalid input. Please run the code again.")

if __name__ == "__main__":
    main()
