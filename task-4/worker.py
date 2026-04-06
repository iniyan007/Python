import time
import json
import redis
from broker import dequeue
from retry import get_backoff_delay
import tasks
import threading

r = redis.Redis(host='localhost', port=6379, db=0)

RETRY_QUEUE = "queue:retry"
DEAD_QUEUE = "queue:dead"

def execute_task(task):
    func = getattr(tasks, task["func"])
    start = time.time()

    try:
        result = func(*task["args"], **task["kwargs"])
        duration = time.time() - start

        r.hset(f"task:{task['id']}", mapping={
            "func": task["func"],
            "status": "SUCCESS",
            "result": str(result),     
            "duration": duration,
            "retries": task["retries"]
        })

        print(f"[WORKER] Task {task['id']} completed in {duration:.2f}s")

    except Exception as e:
        task["retries"] += 1

        if task["retries"] > task["max_retries"]:
            r.lpush(DEAD_QUEUE, json.dumps(task))
            print(f"[WORKER] Task {task['id']} moved to DEAD LETTER ")
            r.hset(f"task:{task['id']}", mapping={
                "func": task["func"],
                "status": "DEAD_LETTER",
                "retries": task["retries"]
            })
        else:
            delay = get_backoff_delay(task["retries"])
            r.zadd("queue:retry", {json.dumps(task): time.time() + delay})
            r.hset(f"task:{task['id']}", mapping={
                "func": task["func"],
                "status": "RETRY",
                "retries": task["retries"]
            })
            print(f"[WORKER] Retry {task['retries']} in {delay}s")


def retry_handler():
    while True:
        now = time.time()
        tasks_due = r.zrangebyscore(RETRY_QUEUE, 0, now)

        for t in tasks_due:
            r.lpush("queue:default", t)
            r.zrem(RETRY_QUEUE, t)

        time.sleep(1)


def worker_loop():
    print("[WORKER] Started and waiting for tasks...") 
    while True:
        print("[WORKER] Waiting...") 
        task = dequeue()
        print(f"[WORKER] Received task: {task}")
        execute_task(task)


if __name__ == "__main__":
    print("[WORKER] Starting worker + retry handler...")
    threading.Thread(target=retry_handler, daemon=True).start() 
    worker_loop()