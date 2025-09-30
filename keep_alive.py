# keep_alive.py
import os
from threading import Thread
from flask import Flask

app = Flask("keep_alive")

@app.route("/")
def index():
    return "Bot is alive!"

def run():
    port = int(os.getenv("PORT", "8080"))
    # host 0.0.0.0 so Render can access it
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
