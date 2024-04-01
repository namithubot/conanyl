# conanyl
A sentiment analysis web app

This is a Flask web application that allows users to upload audio files, transcribe them, and perform sentiment analysis on the transcribed text. The transcription is done using the Deepgram API, and sentiment analysis is performed using the OpenAI API.

## Prerequisites

Before running or deploying this application, make sure you have the following installed:

- Python 3.x
- Flask
- Requests
- Werkzeug
- OpenAI API key
- Deepgram API key
- Azure Text Analytics API key (optional)

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your_username/audio-analysis-app.git
    ```

2. Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `config.json` file in the root directory of the project and add your API keys:

    ```json
    {
        "DEEPGRAM_API_KEY": "YOUR_DEEPGRAM_API_KEY",
        "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY",
    }
    ```

## Usage

To run the application locally, execute the following command in your terminal:

```bash
flask --app main run
```

## Work Done
The application supports two types of file mp3 and wav (we can support other files as well). It works on two or more dialogues as it uses 'diarize' from deepgram which provides support for multiple users. We store the application in uploads folder which is then provided to deepgram for speech to text processing. Once we get the text, we form a list of json. This is done so that it forms a good data structure for any future use case.

The structure is as follow

```json
{
	'speaker': speaker_number,
	'says': dialogue
}
```

This is then used to form the entire dialogue and provided to OpenAPI chat completion API to get the sentiment analysis on it.

## Challenges faced
- The first challenge that was faced was to get data from deepgram. For diarize, deepgram doesn't send the entire data at once. It divides it in words and we need to process it to form the entire dialogue.
- The biggest challenge was to get the prompt right for OpenAPI. I initially wanted a JSON corresponding to each dialogue number. To do that, I provided specifying the format I want the dialogue. This did give satisfactory result, but started some inconsistency on overall analysis of the result.
We ended up with a balance of both at the end.
- There is no temparature parameter to control the level of randomness expectations, which result in a bit of incosistency on the replies for the same prompt.
