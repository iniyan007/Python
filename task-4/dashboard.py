import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def show_dashboard():
    keys = r.keys("task:*")

    if not keys:
        print("No tasks found in Redis ❌")
        return

    print("\n=== Dashboard ===")
    print("+----------+-------------------+--------------+---------+----------+")

    for key in keys:
        data = r.hgetall(key)

        task_id = key.decode().split(":")[1]
        func = data.get(b"func", b"-").decode()
        status = data.get(b"status", b"-").decode()
        retries = data.get(b"retries", b"0").decode()
        duration = data.get(b"duration", b"-").decode()

        print(f"{task_id:10} {func:20} {status:12} {retries:7} {duration:8}")

if __name__ == "__main__":
    show_dashboard()