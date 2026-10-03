import os

from flask import Flask
import redis

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "db-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


@app.route("/")
def index():
    visits = redis_client.incr("hits")

    container_id = os.getenv("HOSTNAME", "unknown")

    return (
        f"Bonjour ! Cette page a été vue {visits} fois. "
        f"Je suis le conteneur {container_id}"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)