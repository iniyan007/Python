# 🚀 Async API Gateway with Rate Limiting, Caching & Circuit Breaker

## 📌 Overview

This project implements an **asynchronous API Gateway** using FastAPI that routes requests to downstream microservices and includes:

- 🔀 Reverse Proxy Routing
- 🚦 Token Bucket Rate Limiting (per API key)
- ⚡ Response Caching with Redis (TTL-based)
- 🔥 Circuit Breaker Pattern for fault tolerance
- 📊 Health Dashboard with service metrics

---

## 🧠 Architecture

```
Client → API Gateway → (Rate Limit → Cache → Circuit Breaker) → Microservices
↓
Redis
```

---

## ⚙️ Tech Stack

- FastAPI (Async framework)
- httpx (Async HTTP client)
- Redis (Caching + Rate limiting)
- Python asyncio

---

## 📁 Project Structure

```

task-6/
│── main.py
│── config.py
│── cache.py
│── circuit_breaker.py
│── rate_limiter.py
│── redis_client.py
│── user-service/
|   |── user-service.py
│── order-service/
|   |── order-service.py
│── product-service/
|   |──product-service.py

```

---

## 🔧 Features

### 🔀 1. Reverse Proxy Routing

Routes incoming requests:

| Endpoint | Service |
|-------|-------|
| `/api/users/**` | user-service |
| `/api/orders/**` | order-service |
| `/api/products/**` | product-service |

---

### 🚦 2. Rate Limiting (Token Bucket)

- Limit: **5 requests/min per API key**
- Uses Redis to track tokens

#### Example:
```
429 Too Many Requests
```

---

### ⚡ 3. Caching (Redis + TTL)

- Only caches GET requests
- TTL: **60 seconds**

#### Example:
```
CACHE HIT (TTL: 51s remaining)
```

---

### 🔥 4. Circuit Breaker

- Opens after **5 consecutive failures**
- Returns **503 Service Unavailable**
- Automatically recovers after timeout

#### Flow:
```
CLOSED → OPEN → HALF-OPEN → CLOSED
```

---

### 📊 5. Health Dashboard

Displays:

- Service status (UP/DOWN)
- Average latency
- Circuit state
- Cache hits

#### Example:
```

=== Health Dashboard ===
+------------------+--------+---------+----------+-------------+
| Service          | Status | Latency | Circuit  | Cache Hits  |
+------------------+--------+---------+----------+-------------+
| user-service     | UP     | 0ms     | CLOSED   | 0           |
| order-service    | DOWN   | 0ms     | CLOSED   | 0           |
| product-service  | UP     | 301ms   | CLOSED   | 4           |
+------------------+--------+---------+----------+-------------+

````

---

## 🧪 Testing

### 🔹 Normal Request

```bash
curl http://localhost:8080/api/products/1
```

---

### 🔹 Cache Test

Run twice:

```bash
curl http://localhost:8080/api/products/1
```

Expected:

```
CACHE HIT
```

---

### 🔹 Rate Limit Test

```bash
for i in {1..10}
do
 curl http://localhost:8080/api/products/1
done
```

Expected:

```
429 Too Many Requests
```

---

### 🔹 Circuit Breaker Test

1. Stop a service:

```bash
CTRL + C (order-service)
```

2. Send requests:

```bash
for i in {1..6}
do
 curl http://localhost:8080/api/orders/latest
done
```

Expected:

```
500 errors → then 503 CIRCUIT OPEN
```

---

## 📜 Sample Logs

```
[REQ] GET /api/products/1 -> PROXY — 200 OK
[REQ] GET /api/products/1 -> CACHE HIT — 200 OK
[REQ] GET /api/products/1 -> RATE LIMITED — 429
[REQ] GET /api/orders/latest -> ERROR — 500
[REQ] GET /api/orders/latest -> CIRCUIT OPEN — 503
```

---

## 🎯 Key Concepts Implemented

* Async programming (async/await)
* Token bucket rate limiting
* Redis caching
* Circuit breaker design pattern
* Reverse proxy architecture
* Middleware design

---

## 🏆 Outcome

This project demonstrates a **production-level API Gateway system** similar to:

* AWS API Gateway
* Kong Gateway
* Netflix Zuul

---
