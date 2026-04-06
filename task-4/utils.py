import uuid
import time

def create_task(func_name, args=None, kwargs=None):
    return {
        "id": str(uuid.uuid4())[:6],
        "func": func_name,
        "args": args or [],
        "kwargs": kwargs or {},
        "status": "PENDING",
        "retries": 0,
        "max_retries": 3,
        "created_at": time.time()
    }