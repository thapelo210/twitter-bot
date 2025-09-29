# bot.py
import os
import tweepy
import schedule
import time
import threading
from flask import Flask
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Setup Twitter Client (v2)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# Generate a short positive tweet using ChatGPT API
def generate_message():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes positive motivational tweets."},
                {"role": "user", "content": "Write a short, catchy, positive motivational tweet under 280 characters."}
            ],
            temperature=0.8,
            max_tokens=60
        )
        text = response['choices'][0]['message']['content'].strip()
        return text[:280]
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return "Stay positive and keep moving forward! 💪"

# Tweet the generated message
def tweet_message():
    msg = generate_message()
    try:
        client.create_tweet(text=msg)
        print(f"✅ Tweeted: {msg}")
    except Exception as e:
        print(f"❌ Twitter API error: {e}")

# Schedule: run every hour
schedule.every().hour.do(tweet_message)

# Tweet once immediately
tweet_message()

# Flask server to keep online (if needed for hosting)
app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_flask).start()

print("🚀 Bot started... tweeting every hour")

# Main loop
while True:
    schedule.run_pending()
    time.sleep(1)
