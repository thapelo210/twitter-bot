# bot.py
import tweepy
from transformers import pipeline
import schedule
import time
import os

API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["ACCESS_SECRET"]


# ==== Twitter API Keys (v2) ====
API_KEY = "rX3VkYdvXtLolPZtpbNIMlaoL"
API_SECRET = "77WqRnVLGos6fX3173X6t8kZ4GBv7YOo3i3CgQ0z5iXy9IKsCK"
ACCESS_TOKEN = "1972573302553214976-7qMkAPzZXvnSpAfsoH2z8TfWBCtikh"
ACCESS_SECRET = "LQRXmEOXbssfPxkYJXn0dtbioLVgs8H4MPXTZLQUJfiAc"

# Setup Tweepy Client for v2
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# Load GPT-2 locally
generator = pipeline("text-generation", model="gpt2")

def generate_message():
    prompt = "Write a short positive motivational message for Twitter:"
    outputs = generator(
        prompt,
        max_new_tokens=40,
        temperature=0.9,
        top_p=0.95,
        do_sample=True
    )
    return outputs[0]["generated_text"].replace(prompt, "").strip()

def tweet_message():
    msg = generate_message()[:250]  # Twitter limit
    try:
        client.create_tweet(text=msg)
        print(f"✅ Tweeted: {msg}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Schedule: run every hour
schedule.every().hour.do(tweet_message)

# Optional: run once immediately
tweet_message()

print("🚀 Bot started... tweeting every hour")
while True:
    schedule.run_pending()
    time.sleep(1)
