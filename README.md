# Speaker's Speaking Rate Application

This is a runbook explaining how to carry out the process related to the verification of the speech rate (or pace) of a speaker in a audio file (local or using an URL), using the AssemblyAI API.

<strong>Note</strong>: For this process, I'm using the Fedora 39, so all the mentioned steps will be refered to the same OS. </ul>

# Prerequisites

You must have some python libraries configured in your enviroment before trying to run those applications·

1. Python
2. Requests
3. Tkinter
4. Logging
5. Sys

```
sudo apt install python3-pip

sudo pip install request

sudo pip install tk

sudo pip install logging

sudo pip install sys
```

# How to run the application (via Terminal)

This application was developed to be used in any IDE that can run a Python file and can read libraries dependencies, such as Visual Studio Code or PyCharm.

# Context

This application has the purpose to transcribe an audio file (by a URL or uploaded via a local file), calculating the speeach rate of a determined file using the AssemblyAI Speech-to-Text API to perform this.


# Application

The application currently consists of a single file that contains all the code necessary to run (except that the variables are in another file, to improve the readability).

<li><strong>audio_coding.py</strong> -> This file has the ability to check the speech rate of any supported audio file (by a URL or via a local file), displaying the info using a simple UI

<strong>Note</strong>: Please access this [URL](https://www.assemblyai.com/docs/speech-to-text/speech-recognition) to check the complete documentation of the API used.

# How to obtain an API to run the application

In order to run this application you will need to create an account on [AssemblyAI](https://www.assemblyai.com/) with a free tier, then, you will be able to access a private API key for usage and the same can work with this application, given that we'll use only the functions available on the same plan.





