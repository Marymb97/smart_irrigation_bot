# Smart Irrigation Advice Chatbot

This project provides a Python chatbot to help beginner farmers decide whether to irrigate their crops using real-time weather data and AI-powered recommendations.

## Features
- Asks for crop type and city
- Retrieves weather data from OpenWeather API
- Uses Gemini (Google Generative AI) for irrigation advice (free tier)
- Beginner-friendly, structured output
- Secure API key management via environment variables
- Error handling and clear documentation

## Setup Instructions
1. Copy `.env.example` to `.env` and add your API keys.
   - Set `OPENWEATHER_API_KEY` to your OpenWeather key.
   - Set `GEMINI_API_KEY` to your Google Generative AI key (or leave blank to use the default provided in code).
2. Install dependencies:
   pip install -r requirements.txt
3. Run the chatbot with Streamlit:
   streamlit run main.py

## Security
- API keys are managed via environment variables in a `.env` file (never commit your real `.env` file).
- Gemini (Google Generative AI) is used by default for free LLM access.

## License
MIT License
