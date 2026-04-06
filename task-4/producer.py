from broker import enqueue
from utils import create_task
from tasks import generate_thumbnail, send_email 

def enqueue_task(func, *args, **kwargs):
    task = create_task(func.__name__, args, kwargs)
    enqueue(task)
    print(f"Task queued: {task}")


if __name__ == "__main__":
    print("[PRODUCER] Sending tasks...")

    enqueue_task(generate_thumbnail, 4521, size=(256,256))
    enqueue_task(send_email, to="bob@co.com", template="welcome")