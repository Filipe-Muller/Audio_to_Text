# Speaker's Speaking Rate Application

This is a runbook explaining how to carry out the process related to the verification of the speech rate (or pace) of a speaker in a audio file (local, URL or real-time streaming).

<ul><li> Note: For this process, I'm using the Ubuntu 20.04 LTS, so all the mentioned steps will be refered to the same OS. </ul>

# Prerequisites

You must have some python libraries configured in your enviroment before trying to run those applications·

1. Python
2. PyAudio
3. Websockets
4. Asyncio
5. Requests

```
sudo apt install python3-pip

sudo pip install pyaudio

sudo pip install websockets

sudo pip install asyncio

sudo pip install requests
```

# How to run the application (via Terminal)

This application was developed to be used in a terminal, the main suggestion is to use an IDE (_VS Code_ was used for this case) and then use the Python compiler as well.

# Context

This application has the purpose to transcribe an audio file (by a URL or uploaded via a local file) and also, to transcribe in real-time (but bear in mind that this part is attached to a paid function in the API).

API used: AssemblyAI Speech-to-Text

# Application

Here we have three .py files, each of them has a specific purpose and they must be selected for the case that suits your requirements.

*audio_coding.py* -> This file has the ability to check the speech rate of any supported audio file (by a URL or via a local file)

*audio_codign_loop.py* -> Has the same function of the previous file, but this application stays in a loop (until the user end him)

*realtime_audio.py* -> This file has the function of transcribe real-time audio and report the speaker speech rate


<ul><li> Note: Please access this URL (https://docs.assemblyai.com/#supported-file-types) to check all the supported format files. </ul>

# Main Approach

As we've several types of audio transcription available in the API, I chose to implement three different ways: upload via URL, via local file and real-time. The idea of the application was to be user orientaded, where we need the input of the user to proceed with the process. 

Instead of having two applications for the URL and local file, I prefered to use one instead and then I made some conditionals there, to fulfill my requests and to align.

![image](https://user-images.githubusercontent.com/85353297/170801647-654d26e7-717d-4381-90f9-e417f34869fa.png)

_Caption: Output in the terminal for the URL application_ 

![image](https://user-images.githubusercontent.com/85353297/170802222-f2ef02d9-1bd2-4725-b479-e44147bbe71c.png)

_Caption: Output in the terminal for the local file application_ 


<ul><li> Note: For the real-time transcription, I couldn't test the application, due do the feature being paid and due to some errors in the Ubuntu enviroment. </ul>

![image](https://user-images.githubusercontent.com/85353297/170802393-03e85ab3-79c4-4141-94bc-e5a69f0d5988.png)


_Caption: Output in the terminal, errors in the process (paid feature and enviroment issues)_




