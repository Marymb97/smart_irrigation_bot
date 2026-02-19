"""
main.py - Smart Irrigation Advice Chatbot

This chatbot helps beginner farmers decide whether to irrigate their crops using real-time weather data and AI-powered recommendations.
"""
import os
import requests
from dotenv import load_dotenv


import streamlit as st
import google.generativeai as genai

# Load environment variables from .env in the script directory, regardless of working directory
from pathlib import Path
dotenv_path = Path(__file__).parent / ".env"
import dotenv
dotenv.load_dotenv(dotenv_path=dotenv_path, override=True)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def get_weather(city):
    """Retrieve current weather data for a city from OpenWeather API."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            return {"error": "City not found. Please check the city name."}
        response.raise_for_status()
        data = response.json()
        weather = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "precipitation": data.get("rain", {}).get("1h", 0),
            "description": data["weather"][0]["description"],
        }
        return weather
    except requests.exceptions.RequestException as e:
        return {"error": f"Network or API error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


def get_irrigation_advice(crop, city, weather):
    """Send crop and weather data to LLM for irrigation advice."""
    prompt = (
        f"You are an agricultural assistant for beginner farmers. "
        f"Given the following data, provide a clear, structured irrigation recommendation.\n"
        f"Crop: {crop}\n"
        f"Location: {city}\n"
        f"Temperature: {weather['temperature']}°C\n"
        f"Humidity: {weather['humidity']}%\n"
        f"Precipitation (last hour): {weather['precipitation']} mm\n"
        f"Weather: {weather['description']}\n"
        "\n"
        "IMPORTANT: Your response MUST be in this exact format, with no extra text, no introduction, and no summary.\n"
        "[IRRIGATION_NEEDED]\nYes or No\n[/IRRIGATION_NEEDED]\n"
        "[REASONING]\nShort, clear explanation\n[/REASONING]\n"
        "[SUGGESTED_FREQUENCY]\nHow often to water\n[/SUGGESTED_FREQUENCY]\n"
        "[PRECAUTIONS]\nSimple, practical precautions\n[/PRECAUTIONS]\n"
        "Do not add any other text. Do not add a greeting or closing."
    )
    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        response = model.generate_content(prompt)
        if hasattr(response, 'text') and response.text.strip():
            return response.text.strip()
        # Fallback: try a more forceful prompt if the first response is empty
        fallback_prompt = (
            f"You must answer in this format, with no extra text.\n"
            f"[IRRIGATION_NEEDED]\nYes or No\n[/IRRIGATION_NEEDED]\n"
            f"[REASONING]\nShort, clear explanation\n[/REASONING]\n"
            f"[SUGGESTED_FREQUENCY]\nHow often to water\n[/SUGGESTED_FREQUENCY]\n"
            f"[PRECAUTIONS]\nSimple, practical precautions\n[/PRECAUTIONS]\n"
            f"Crop: {crop}\nLocation: {city}\nTemperature: {weather['temperature']}°C\nHumidity: {weather['humidity']}%\nPrecipitation: {weather['precipitation']} mm\nWeather: {weather['description']}\n"
        )
        response2 = model.generate_content(fallback_prompt)
        if hasattr(response2, 'text'):
            return response2.text.strip()
        else:
            return str(response2)
    except Exception as e:
        import traceback
        import streamlit as st
        st.error(f"[AI Exception] {e}\n{traceback.format_exc()}")
        return f"[AI Exception] {e}"


def main():
    st.set_page_config(page_title="Smart Irrigation Advice Chatbot", page_icon="💧")
    if not GEMINI_API_KEY:
        st.error("AI API key is missing or revoked. Add a new key to your .env file and restart the app.")
        st.stop()
    # App Title and Subtitle
    st.markdown(
        """
        <style>
        .welcome-premium {
            background: linear-gradient(135deg, #23293a 60%, #2a8cff 100%);
            border-radius: 22px;
            box-shadow: 0 8px 40px 0 rgba(42,140,255,0.18), 0 0 0 2px #2a8cff33;
            border: 1.5px solid #2a8cff55;
            padding: 2.5em 2.5em 2.2em 2.5em;
            margin: 2.5em auto 2em auto;
            max-width: 600px;
            animation: cardFadeIn 1.1s cubic-bezier(.4,1.6,.6,1);
            position: relative;
            overflow: hidden;
            text-align: center;
        }
        @keyframes cardFadeIn {
            from { opacity: 0; transform: translateY(40px) scale(0.98); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .welcome-premium .placeholder-title {
            font-size: 1.5em;
            color: #b0c4de;
            font-weight: 800;
            margin-bottom: 0.3em;
            letter-spacing: 0.01em;
            text-shadow: 0 2px 12px #2a8cff33;
        }
        .welcome-premium .placeholder-desc {
            font-size: 1.13em;
            color: #cfd8dc;
            font-weight: 500;
            margin-bottom: 0.5em;
            line-height: 1.7em;
        }
        .welcome-premium .placeholder-svg {
            margin-bottom: 1.2em;
            filter: drop-shadow(0 2px 16px #2a8cff44);
            animation: svgFloat 2.8s ease-in-out infinite alternate;
        }
        @keyframes svgFloat {
            from { transform: translateY(0); }
            to { transform: translateY(-12px); }
        }
        </style>
        <div style='text-align: center; margin-bottom: 1.5em;'>
            <h1 style='font-size:2.6em; font-weight:800; color:#2a8cff; margin-bottom:0.2em; letter-spacing:0.01em;'>
                Smart Irrigation Advice Chatbot
            </h1>
            <div style='font-size:1.25em; color:#e0e0e0; font-weight:500; margin-bottom:0.2em;'>
                Personalized, weather-aware watering guidance for your crops
            </div>
        </div>
        <div class='welcome-premium'>
            <svg class='placeholder-svg' width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                <ellipse cx="40" cy="60" rx="22" ry="8" fill="#b3e5fc"/>
                <path d="M40 12C40 12 22 36 22 48C22 59.0457 30.9543 68 42 68C53.0457 68 62 59.0457 62 48C62 36 40 12 40 12Z" fill="url(#paint0_linear)"/>
                <defs>
                    <linearGradient id="paint0_linear" x1="40" y1="12" x2="40" y2="68" gradientUnits="userSpaceOnUse">
                        <stop stop-color="#2a8cff"/>
                        <stop offset="1" stop-color="#6dd5ed"/>
                    </linearGradient>
                </defs>
            </svg>
            <div class='placeholder-title'>Welcome to your Smart Irrigation Advisor!</div>
            <div class='placeholder-desc'>Enter your crop and city below to receive beautiful, personalized watering advice powered by real-time weather and AI.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Sidebar
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif !important;
        }
        .stTextInput>div>div>input {
            font-size: 1.1em;
            background: #23272f !important;
            color: #e0e0e0 !important;
            border-radius: 8px !important;
            border: 1.5px solid #2a8cff33 !important;
            transition: border 0.2s, box-shadow 0.2s;
        }
        .stTextInput>div>div>input:focus {
            border: 1.5px solid #2a8cff !important;
            box-shadow: 0 0 0 2px #2a8cff33 !important;
        }
        .stButton>button {
            font-size: 1.1em;
            background: linear-gradient(90deg, #2a8cff 60%, #6dd5ed 100%);
            color: white;
            border-radius: 8px;
            transition: 0.2s;
            border: none;
            box-shadow: 0 2px 8px 0 rgba(42,140,255,0.10);
            padding: 0.7em 1.7em;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #6dd5ed 0%, #2a8cff 100%);
            box-shadow: 0 4px 16px 0 rgba(42,140,255,0.18);
        }
        .stAlert {border-radius: 8px;}
        .card {
            background: #181c24;
            border-radius: 18px;
            box-shadow: 0 8px 32px 0 rgba(42,140,255,0.13);
            padding: 2.2em 2.7em 2.2em 2.7em;
            margin: 2.5em auto 2em auto;
            max-width: 600px;
            border: 1.5px solid #23272f;
            animation: fadeIn 0.7s;
        }
        @media (max-width: 700px) {
            .card { padding: 1.2em 0.5em 1.2em 0.5em; }
            .advice-box { padding: 1.2em 0.5em 1.2em 0.5em !important; }
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .weather-box {
            background: #eaf6ff;
            border-radius: 12px;
            padding: 1.2em 1.5em 1.2em 1.5em;
            margin-bottom: 1.5em;
            font-size: 1.15em;
            color: #1a1a1a;
            box-shadow: 0 2px 12px 0 rgba(42,140,255,0.07);
            font-weight: 500;
        }
        .weather-box b, .weather-box span {color: #1a1a1a;}
        .advice-box {
            background: #f6fafd;
            border-radius: 12px;
            padding: 1.2em 1.5em 1.2em 1.5em;
            font-size: 1.13em;
            border: 1px solid #e0e0e0;
            color: #23272f;
            box-shadow: 0 2px 12px 0 rgba(42,140,255,0.06);
            margin-bottom: 2em;
            line-height: 1.7em;
            animation: fadeIn 0.7s;
        }
        .copy-btn {
            display: inline-block;
            margin: 0.5em 0 1.5em 0;
            padding: 0.5em 1.2em;
            background: linear-gradient(90deg, #2a8cff 60%, #6dd5ed 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        .copy-btn:hover {
            background: linear-gradient(90deg, #6dd5ed 0%, #2a8cff 100%);
        }
        .section-title {
            font-size: 1.45em;
            font-weight: 700;
            color: #2a8cff;
            margin-bottom: 0.5em;
            display: flex;
            align-items: center;
            gap: 0.5em;
            letter-spacing: 0.01em;
        }
        /* Center the form card on all screens */
        .main .block-container { display: flex; flex-direction: column; align-items: center; }
        </style>
    """, unsafe_allow_html=True)

    with st.form("input_form", clear_on_submit=False):
        # Only show the two intended input fields
        crop = st.text_input("🌱 What are you growing?", placeholder="e.g. rice, wheat, maize", key="crop_input")
        city = st.text_input("📍 Where are your crops? (City)", placeholder="e.g. Krakow", key="city_input")
        submitted = st.form_submit_button("Show me my watering advice")
        # No card placeholder needed; welcome is now at the top

    if submitted:
        if not crop or not city:
            st.error("❗ Both crop type and city are required.")
            return
        with st.spinner("🔎 Retrieving weather data..."):
            weather = get_weather(city)
        if weather is None or "error" in weather:
            st.error("❗ " + (weather["error"] if weather and "error" in weather else "Could not retrieve weather data. Please check your city name and try again."))
            return
        st.markdown(f"""
            <div class='card weather-box'>
                <span class='section-title'>🌤️ Weather in {city.title()}:</span>
                <span><b>{weather['temperature']}°C</b>, <b>{weather['humidity']}%</b> humidity, <b>{weather['precipitation']} mm</b> rain, <b>{weather['description'].capitalize()}</b></span>
            </div>
            <div style='height: 0.5em;'></div>
            <div style='color:#2a8cff; font-size:1.05em; margin-bottom:0.5em;'>Here's what the weather means for your crops today:</div>
        """, unsafe_allow_html=True)
        with st.spinner("🤖 Getting irrigation advice from AI..."):
            try:
                advice = get_irrigation_advice(crop, city, weather)
            except Exception as e:
                advice = None
                st.error("Sorry, there was an error getting advice. Please try again.")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<span class='section-title'>📝 Your Watering Advice</span>", unsafe_allow_html=True)
        if advice:
            import re
            # Try to extract using new explicit section markers
            irrigation = re.search(r"\[IRRIGATION_NEEDED\](.*?)\[/IRRIGATION_NEEDED\]", advice, re.DOTALL)
            reasoning = re.search(r"\[REASONING\](.*?)\[/REASONING\]", advice, re.DOTALL)
            freq = re.search(r"\[SUGGESTED_FREQUENCY\](.*?)\[/SUGGESTED_FREQUENCY\]", advice, re.DOTALL)
            precautions = re.search(r"\[PRECAUTIONS\](.*?)\[/PRECAUTIONS\]", advice, re.DOTALL)

            def clean_section(match, default):
                return match.group(1).strip() if match and match.group(1).strip() else default

            irrigation_val = clean_section(irrigation, "No clear answer")
            reasoning_val = clean_section(reasoning, "No reasoning provided.")
            freq_val = clean_section(freq, "No frequency advice provided.")
            precautions_val = clean_section(precautions, "No precautions provided.")

            # Compose advice text for copying
            advice_text = f"Should you water today?\n{irrigation_val}\n\nWhy this advice?\n{reasoning_val}\n\nHow often to water?\n{freq_val}\n\nThings to watch out for\n{precautions_val}"

            # Download Advice button (universal, robust)
            st.markdown("""
            <style>
            .stDownloadButton > button {
                background: linear-gradient(90deg, #2a8cff 60%, #6dd5ed 100%) !important;
                color: white !important;
                border-radius: 8px !important;
                font-size: 1.08em !important;
                font-weight: 700 !important;
                padding: 0.7em 1.7em !important;
                margin-top: 1.2em !important;
                margin-bottom: 0.5em !important;
                box-shadow: 0 2px 8px 0 rgba(42,140,255,0.10) !important;
                border: none !important;
                transition: background 0.2s !important;
            }
            .stDownloadButton > button:hover {
                background: linear-gradient(90deg, #6dd5ed 0%, #2a8cff 100%) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            st.download_button(
                label="💾 Download Advice as .txt",
                data=advice_text,
                file_name="watering_advice.txt",
                mime="text/plain",
                help="Download the advice as a text file.",
                key="download_advice_btn"
            )
            st.markdown(f"""
            <div class='card advice-box' style='padding:2.5em 2.5em 2.2em 2.5em; background: #181c24; border-radius: 20px; box-shadow: 0 8px 32px 0 rgba(42,140,255,0.13); margin-bottom: 2em;'>
                <div style='background: #23293a; border-radius: 14px; padding: 1.2em 1.5em 1.2em 1.5em; margin-bottom: 1.5em; animation: fadeIn 0.7s;'>
                    <div style='display:flex;align-items:center;gap:0.7em;margin-bottom:0.7em;'>
                        <span style='font-size:2em;'>💧</span>
                        <span style='font-size:1.35em;font-weight:700;color:#2a8cff;'>Should you water today?</span>
                    </div>
                    <div style='font-size:1.25em;font-weight:700;margin-bottom:0.3em; color:{'#2ecc40' if irrigation_val.strip().lower() == 'yes' else '#ff4b4b'};'>
                        {irrigation_val}
                    </div>
                </div>
                <div style='background: #20242f; border-radius: 14px; padding: 1.2em 1.5em 1.2em 1.5em; margin-bottom: 1.5em; animation: fadeIn 1.1s;'>
                    <div style='display:flex;align-items:center;gap:0.7em;margin-bottom:0.5em;'>
                        <span style='font-size:1.5em;'>🧠</span>
                        <span style='font-size:1.13em;font-weight:700;color:#2a8cff;'>Why this advice?</span>
                    </div>
                    <div style='color:#e0e0e0;font-size:1.12em;'>{reasoning_val}</div>
                </div>
                <div style='background: #20242f; border-radius: 14px; padding: 1.2em 1.5em 1.2em 1.5em; margin-bottom: 1.5em; animation: fadeIn 1.5s;'>
                    <div style='display:flex;align-items:center;gap:0.7em;margin-bottom:0.5em;'>
                        <span style='font-size:1.5em;'>⏰</span>
                        <span style='font-size:1.13em;font-weight:700;color:#2a8cff;'>How often to water?</span>
                    </div>
                    <div style='color:#e0e0e0;font-size:1.12em;'>{freq_val}</div>
                </div>
                <div style='background: #20242f; border-radius: 14px; padding: 1.2em 1.5em 1.2em 1.5em; animation: fadeIn 1.9s;'>
                    <div style='display:flex;align-items:center;gap:0.7em;margin-bottom:0.5em;'>
                        <span style='font-size:1.5em;'>⚠️</span>
                        <span style='font-size:1.13em;font-weight:700;color:#2a8cff;'>Things to watch out for</span>
                    </div>
                    <div style='color:#e0e0e0;font-size:1.12em;'>{precautions_val}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No advice was returned. Please try again.")


if __name__ == "__main__":
    main()
