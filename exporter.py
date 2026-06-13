import time
import requests
from prometheus_client import start_http_server, Gauge

TARGET_URL = "http://34.201.58.43:32500/api/latest-confidence"

confidence_gauge = Gauge(
    "prediction_confidence_score",
    "Latest model prediction confidence score"
)

def poll():
    while True:
        try:
            r = requests.get(TARGET_URL, timeout=5)
            data = r.json()
            confidence_gauge.set(float(data.get("confidence", 1.0)))
        except Exception:
            confidence_gauge.set(1.0)
        time.sleep(5)

if __name__ == "__main__":
    start_http_server(8000)
    poll()