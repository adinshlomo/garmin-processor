# Garmin Run Recommendation API

This project fetches your Garmin Connect data and provides a personalized running recommendation using ChatGPT.

## Setup

1. Create `.env` from `.env.example` and fill in your credentials.
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the API:
    ```
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```
4. Call `/get-run` to fetch your data and receive a run recommendation.

## Deploying to Render

- Create a new Web Service
- Use this repo as your source
- Set environment variables in Render from `.env`

#   g a r m i n - p r o c e s s o r  
 