import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import tweepy

# .env読み込み
load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Tweepyクライアント
client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True
)

app = Flask(__name__)

def validate_message(msg: str):
    if not msg:
        return False, "msgパラメータが必要です"
    msg = msg.strip()
    if len(msg) == 0:
        return False, "空文字は不可です"
    if len(msg) > 280:
        return False, "280文字以内にしてください"
    return True, msg

@app.route("/tweet", methods=["GET"])
def tweet():
    raw_msg = request.args.get("msg")
    ok, result = validate_message(raw_msg)
    if not ok:
        return jsonify({"ok": False, "error": result}), 400

    try:
        resp = client.create_tweet(text=result)
        return jsonify({"ok": True, "tweet_id": resp.data.get("id"), "text": result}), 201
    except tweepy.TweepyException as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)