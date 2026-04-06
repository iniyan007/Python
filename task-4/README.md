# 🚀 Distributed Task Queue using Redis (Python)

## 📌 Overview

This project implements a **distributed task queue system** using Python and Redis. It follows the **producer-consumer pattern**, where tasks are queued and processed asynchronously by multiple workers.

The system supports:

* Task distribution across workers
* Retry mechanism with exponential backoff
* Dead Letter Queue (DLQ) for failed tasks
* Result backend using Redis
* CLI dashboard for monitoring

---

## 🧠 Architecture

```
Producer → Redis Queue → Worker → Result Backend
                          ↓
                     Retry Queue
                          ↓
                   Dead Letter Queue
```

---

## ⚙️ Technologies Used

* Python
* Redis (`redis-py`)
* JSON serialization
* Threading
* Multiprocessing (conceptually supported)

---

## 📂 Project Structure

```
task_queue/
│
├── broker.py        # Redis queue operations
├── producer.py      # Task producer
├── worker.py        # Worker + retry handler
├── tasks.py         # Task functions
├── utils.py         # Task creation
├── retry.py         # Backoff logic
├── dashboard.py     # CLI dashboard
```

---

## 🔧 Redis Data Structures

| Purpose           | Redis Key     | Type |
| ----------------- | ------------- | ---- |
| Main Queue        | queue:default | LIST |
| Retry Queue       | queue:retry   | ZSET |
| Dead Letter Queue | queue:dead    | LIST |
| Task Results      | task:<id>     | HASH |

---

## 🚀 How It Works

### 1. Producer

* Creates tasks
* Pushes them to Redis queue

```python
enqueue_task(generate_thumbnail, 4521, size=(256,256))
enqueue_task(send_email, to="bob@co.com", template="welcome")
```

---

### 2. Worker

* Continuously polls queue
* Executes tasks
* Stores results in Redis

---

### 3. Retry Mechanism

* On failure → retries task
* Uses exponential backoff:

```
2s → 4s → 8s
```

---

### 4. Dead Letter Queue (DLQ)

* If retries exceed limit
* Task is moved to:

```
queue:dead
```

---

### 5. Result Backend

Each task is stored as:

```
task:<id> → {
    func,
    status,
    retries,
    duration,
    result
}
```

---

## 📊 Dashboard

Run:

```bash
python dashboard.py
```

### Example Output

```
=== Dashboard ===
+----------+-------------------+--------------+---------+----------+
7266f9     generate_thumbnail  SUCCESS        0         1.00
f876bf     send_email          DEAD_LETTER    3         -
```

---

## 🧪 Running the Project

### 1. Start Redis

```bash
redis-server
```

---

### 2. Start Worker

```bash
python worker.py
```

---

### 3. Run Producer

```bash
python producer.py
```

---

### 4. View Dashboard

```bash
python dashboard.py
```

---

## 🔁 Example Execution Flow

```
[WORKER] Picked task generate_thumbnail
[WORKER] Task completed

[WORKER] Picked task send_email
[WORKER] Retry 1 in 2s
[WORKER] Retry 2 in 4s
[WORKER] Task completed
```

---

## 🔥 Features Implemented

✅ Distributed task execution
✅ Redis-based message broker
✅ Exponential retry mechanism
✅ Dead Letter Queue (DLQ)
✅ Result backend
✅ CLI dashboard

---

## 🧹 Clear Redis (Optional)

```bash
redis-cli FLUSHALL
```

---

## 🏁 Conclusion

This project demonstrates a **production-style distributed system** similar to Celery, showcasing:

* Asynchronous processing
* Fault tolerance
* Scalable architecture
