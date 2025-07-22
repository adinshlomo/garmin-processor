import os
from fastapi import FastAPI
from pydantic import BaseModel
from garminconnect import Garmin
import openai
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("adinshlomo@gmail.com")
PASSWORD = os.getenv("Adin2005")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class RunRecommendation(BaseModel):
    data: dict
    recommendation: str

def get_garmin_data():
    client = Garmin(EMAIL, PASSWORD)
    client.login()

    data = {
        "last_activity": client.get_last_activity(),
        "training_readiness": client.get_training_readiness(),
        "training_status": client.get_training_status(),
        "resting_heart_rate": client.get_rhr(),
        "sleep_data": client.get_sleep_data("today"),
        "body_battery": client.get_body_battery("today"),
        "hrv": client.get_hrv_data("today"),
        "stress": client.get_stress_data("today"),
        "vo2_max": client.get_max_metrics(),
        "endurance_score": client.get_endurance_score("today"),
        "race_predictions": client.get_race_predictions(),
        "last_7_day_activities": client.get_activities(0, 7)
    }
    return data

def get_recommendation(data):
    openai.api_key = OPENAI_API_KEY
    prompt = (
        "You are a personal running coach.Based on the user's recent Garmin data, "
        "suggest a run plan for the next 72 hours. Be concise, practical, and safe. "
        "Limit to 30 words. Data:\n" + str(data)
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful and experienced running coach."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

@app.get("/get-run", response_model=RunRecommendation)
def get_run():
    try:
        data = get_garmin_data()
        recommendation = get_recommendation(data)
        return {"data": data, "recommendation": recommendation}
    except Exception as e:
        return {"data": {}, "recommendation": f"Error: {str(e)}"}
