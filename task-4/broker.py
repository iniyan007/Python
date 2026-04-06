import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = "queue:default"

def enqueue(task):
    r.lpush(QUEUE_NAME, json.dumps(task))

def dequeue():
    _, task = r.brpop(QUEUE_NAME)
    return json.loads(task)