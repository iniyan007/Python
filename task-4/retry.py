import time

def get_backoff_delay(retry_count):
    return 2 ** retry_count  # 2, 4, 8...