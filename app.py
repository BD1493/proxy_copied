from flask import Flask, jsonify
import threading
import time
import os
import getproxy

app = Flask(__name__)

PROXY_DIR = "proxies"


def update_proxies_loop():
    while True:
        try:
            getproxy.main()  # run the scraper
        except Exception as e:
            print("Proxy update error:", e)
        time.sleep(3600)  # refresh every 1 hour


@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "endpoints": [
            "/proxies/http",
            "/proxies/socks4",
            "/proxies/socks5"
        ]
    })


@app.route("/proxies/<ptype>")
def proxies(ptype):
    file_path = os.path.join(PROXY_DIR, f"{ptype}.txt")
    if not os.path.exists(file_path):
        return jsonify({"error": "proxy type not found"}), 404

    with open(file_path, "r") as f:
        data = f.read().splitlines()

    return jsonify({
        "type": ptype,
        "count": len(data),
        "proxies": data
    })


if __name__ == "__main__":
    threading.Thread(target=update_proxies_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)
