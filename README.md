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
