import argparse
import time
from collections import defaultdict, deque


def main() -> None:
    parser = argparse.ArgumentParser(description="Bot anti-scraping (Flask)")
    parser.add_argument("--demo", action="store_true", help="Mode demo sans serveur")
    args = parser.parse_args()

    window = 1.0
    limit = 10
    buckets = defaultdict(lambda: deque())

    def is_rate_limited(ip: str) -> bool:
        now = time.time()
        dq = buckets[ip]
        while dq and now - dq[0] > window:
            dq.popleft()
        dq.append(now)
        return len(dq) > limit

    if args.demo:
        ip = "203.0.113.42"
        for i in range(1, 13):
            status = "429" if is_rate_limited(ip) else "200"
            print(f"Requete {i}: {status}")
        return

    try:
        from flask import Flask, request, jsonify
    except Exception:
        print("Flask requis. Installez: pip install flask")
        print("Astuce: relancez avec --demo pour une demo.")
        return

    app = Flask(__name__)

    @app.route("/")
    def index():
        ip = request.remote_addr or "unknown"
        if is_rate_limited(ip):
            return jsonify({"error": "rate_limited"}), 429
        return jsonify({"status": "ok", "ip": ip})

    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
