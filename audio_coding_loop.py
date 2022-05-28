import requests
import json
from rich import print

while(1):

    # Selecting the type of upload (URL or local file)
    method = input(
        "\nType 1 to upload a file by URL or type 2 to upload a local file: ")

    # URL upload
    if(method == '1'):
        url = input(
            "\nPlease insert the URL where the desired audio file for transcription is located: ")

        print('\nPlease wait until your audio transcription is completed...')

        base_endpoint = "https://api.assemblyai.com/v2/transcript"
        json = {
            "audio_url": url
        }
        headers = {
            "authorization": "a47eb48ba4194ef0b0c875c21a41e1bd",
            "content-type": "application/json"
        }
        response = requests.post(base_endpoint, json=json, headers=headers)
        audio_id = response.json()['id']
        endpoint = base_endpoint + "/" + audio_id

        # Response (url)
        headers = {
            "authorization": "a47eb48ba4194ef0b0c875c21a41e1bd"
        }
        response = requests.get(endpoint, headers=headers)

        while(response.json()['status'] == 'processing'):
            headers = {"authorization": "a47eb48ba4194ef0b0c875c21a41e1bd"}
            response = requests.get(endpoint, headers=headers)

        # Speaker's speaking rate check (local file)
        time_audio = (int(response.json()['audio_duration'])/60)
        words = response.json()['text']
        count_words = words.split()
        total_words = int(len(count_words))
        pace = total_words/time_audio

        if(pace > 160):
            print("\nThe speaker's speaking rate is too fast!\n")

        elif(pace < 120):
            print("\nThe speaker's speaking rate is too slow!\n")

        else:
            print("\nThe speaker's speaking rate is OK!\n")

    # Local file upload
    elif(method == '2'):
        filename = input(
            "\nPlease insert the local file path and the name of the file (with the format) desired for transcription is located: ")

        print('\nPlease wait until your audio transcription is completed...')

        def read_file(filename, chunk_size=5242880):
            with open(filename, 'rb') as _file:
                while True:
                    data = _file.read(chunk_size)
                    if not data:
                        break
                    yield data

        headers = {'authorization': "a47eb48ba4194ef0b0c875c21a41e1bd"}
        response_upload = requests.post(
            'https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(filename))
        endpoint_upload = response_upload.json()['upload_url']

        endpoint = "https://api.assemblyai.com/v2/transcript"
        json = {"audio_url": endpoint_upload}
        headers = {
            "authorization": "a47eb48ba4194ef0b0c875c21a41e1bd",
            "content-type": "application/json"
        }
        response = requests.post(endpoint, json=json, headers=headers)

        audio_id = response.json()['id']
        endpoint = endpoint + "/" + audio_id

        # Response (local file)
        headers = {
            "authorization": "a47eb48ba4194ef0b0c875c21a41e1bd"
        }
        response = requests.get(endpoint, headers=headers)

        while(response.json()['status'] == 'processing'):
            headers = {"authorization": "a47eb48ba4194ef0b0c875c21a41e1bd"}
            response = requests.get(endpoint, headers=headers)

        # Speaker's speaking rate check (local file)
        time_audio = (int(response.json()['audio_duration'])/60)
        words = response.json()['text']
        count_words = words.split()
        total_words = int(len(count_words))
        pace = total_words/time_audio

        if(pace > 160):
            print("\nThe speaker's speaking rate is too fast!\n")

        elif(pace < 120):
            print("\nThe speaker's speaking rate is too slow!\n")

        else:
            print("\nThe speaker's speaking rate is OK!\n")

    else:
        print("\nInvalid input, please run the code again!\n")
