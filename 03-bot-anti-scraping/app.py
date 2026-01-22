import time
from collections import defaultdict, deque


def main() -> None:
    try:
        from flask import Flask, request, jsonify
    except Exception:
        print("Flask requis. Installez: pip install flask")
        return

    app = Flask(__name__)
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

    @app.route("/")
    def index():
        ip = request.remote_addr or "unknown"
        if is_rate_limited(ip):
            return jsonify({"error": "rate_limited"}), 429
        return jsonify({"status": "ok", "ip": ip})

    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
