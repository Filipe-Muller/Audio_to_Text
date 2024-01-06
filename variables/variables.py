# Constants
API_KEY = "<API_KEY>"
UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
SPEAKING_RATE_THRESHOLD_FAST = 160
SPEAKING_RATE_THRESHOLD_SLOW = 120

# Messages
UPLOAD_PROCESSING_MESSAGE = "Please wait while your audio transcription is being processed..."
SPEAKING_RATE_FAST_MESSAGE = "The speaker's speaking rate is too fast."
SPEAKING_RATE_SLOW_MESSAGE = "The speaker's speaking rate is too slow."
SPEAKING_RATE_ACCEPTABLE_MESSAGE = "The speaker's speaking rate is within the acceptable range."
INVALID_INPUT_MESSAGE = "Invalid input. Please try again."
FILE_EXTRACTION_FAILED = "Failed to extract transcript. Please check the provided audio URL or file."
METHOD_PROMPT = "Type 1 to upload a file via URL or type 2 to upload a local file: "
URL_PROMPT = "Please enter the URL where the desired audio file for transcription is located: "
FILENAME_PROMPT = "Please enter the local file path and name (including the format) of the audio file for transcription: "
APP_LABEL = "Select the preferred method to review the speech rate of the desired audio"
URL_OPTION = "1. Upload a URL"
FILE_OPTION = "2. Upload a Local File"
APP_NAME = "Speech Rate App"