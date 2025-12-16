import time
import redis
from flask import Flask

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379)

def get_vote_count():
    retries = 5
    while True:
        try:
            return cache.incr('votes')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_vote_count()
    return '<h1 style="color:blue">Система голосования</h1><p>Голосов за кандидата А: <strong>{}</strong></p>'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)