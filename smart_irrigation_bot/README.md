# Smart Irrigation Advice Chatbot

Smart, beginner-friendly irrigation advice powered by real-time weather data and an AI assistant. The app helps users decide whether to water today, explains the reasoning, recommends frequency, and highlights precautions.

## Features
- Crop and city inputs
- Live weather lookup
- AI-generated, structured advice
- Clear, card-based UI
- Download advice as a .txt file
- Input validation and error handling

## Requirements
- Python 3.10+ (tested on 3.12)
- pip

## Setup
1. Copy `.env.example` to `.env`.
2. Add your API keys in `.env`:
   - `OPENWEATHER_API_KEY`
   - `GEMINI_API_KEY`
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   streamlit run main.py
   ```

## Usage
1. Enter crop type and city.
2. Click the submit button.
3. Review the advice card and download the advice if needed.

## Project Structure
```
smart_irrigation_bot/
├── main.py
├── requirements.txt
├── README.md
├── .env.example
└── .vscode/
```

## Security
- Keep `.env` private.
- Rotate keys if they are ever exposed.

## License
MIT License
