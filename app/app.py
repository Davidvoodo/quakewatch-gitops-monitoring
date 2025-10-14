from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)
REQUESTS = Counter('quakewatch_requests_total', 'Total HTTP requests', ['endpoint'])

@app.route('/')
def index():
    REQUESTS.labels(endpoint="/").inc()
    return jsonify({"status": "ok", "service": "QuakeWatch", "time": time.time()})

@app.route('/healthz')
def health():
    REQUESTS.labels(endpoint="/healthz").inc()
    return "ok", 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
