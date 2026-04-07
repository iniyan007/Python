from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import time

from config import ROUTES
from rate_limiter import is_rate_limited
from cache import get_cache_with_ttl, set_cache
from circuit_breaker import is_open, record_failure, record_success, circuit_state

app = FastAPI()


print("=== Gateway Startup ===")
print("[INFO] API Gateway running on http://0.0.0.0:8080")
for k, v in ROUTES.items():
    print(f"[INFO] Route: /api/{k}/** -> {v}")



metrics = {
    "user-service": {"hits": 0, "latency": [], "status": "UP"},
    "order-service": {"hits": 0, "latency": [], "status": "UP"},
    "product-service": {"hits": 0, "latency": [], "status": "UP"},
}



def log_request(method, path, client, message, status, latency):
    print(f"[REQ] {method} {path} client={client} -> {message} — {status} in {latency}ms")



@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    api_key = request.headers.get("x-api-key", "anonymous")

    limited, tokens = await is_rate_limited(api_key)

    if limited:
        print(f"[REQ] {request.method} {request.url.path} client={api_key} -> RATE LIMITED ({int(tokens)}/{50}) — 429 Too Many Requests")

        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded"}
        )

    return await call_next(request)



@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(service: str, path: str, request: Request):
    start = time.time()
    api_key = request.headers.get("x-api-key", "anonymous")

    if service not in ROUTES:
        return JSONResponse(status_code=404, content={"error": "Service not found"})

    SERVICE_MAP = {
    "users": "user-service",
    "orders": "order-service",
    "products": "product-service"
    }

    service_name = SERVICE_MAP[service]

    target_url = f"{ROUTES[service]}/{service}/{path}" if path else f"{ROUTES[service]}/{service}"

    if is_open(service):
        print(f"[REQ] {request.method} {request.url.path} client={api_key} -> CIRCUIT OPEN ({service_name}) — 503 Service Unavailable")

        return JSONResponse(
            status_code=503,
            content={
                "error": "Service temporarily unavailable",
                "retry_after": 30
            }
        )


    if request.method == "GET":
        cached, ttl = await get_cache_with_ttl(request.method, str(request.url))

        if cached:
            latency = int((time.time() - start) * 1000)

            metrics[service_name]["hits"] += 1

            log_request(
                request.method,
                request.url.path,
                api_key,
                f"CACHE HIT (TTL: {ttl}s remaining)",
                "200 OK",
                latency
            )

            return JSONResponse(content=cached)


    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            body = await request.body()

            response = await client.request(
                method=request.method,
                url=target_url,
                headers=request.headers.raw,
                content=body
            )

        data = response.json()


        if request.method == "GET":
            await set_cache(request.method, str(request.url), data)

        record_success(service)

        latency = int((time.time() - start) * 1000)


        metrics[service_name]["latency"].append(latency)
        metrics[service_name]["status"] = "UP"

        log_request(
            request.method,
            request.url.path,
            api_key,
            f"PROXY to {service_name}",
            f"{response.status_code} OK",
            latency
        )

        return JSONResponse(status_code=response.status_code, content=data)

    except Exception:
        record_failure(service)

        latency = int((time.time() - start) * 1000)

        metrics[service_name]["status"] = "DOWN"

        print(f"[REQ] {request.method} {request.url.path} client={api_key} -> ERROR ({service_name}) — 500 in {latency}ms")

        return JSONResponse(
            status_code=500,
            content={"error": "Downstream service error"}
        )


@app.get("/health")
async def health():
    print("\n=== Health Dashboard ===")
    print("+------------------+--------+---------+----------+-------------+")
    print("| Service          | Status | Latency | Circuit  | Cache Hits  |")
    print("+------------------+--------+---------+----------+-------------+")

    for service in metrics:
        latencies = metrics[service]["latency"]

        avg_latency = f"{int(sum(latencies)/len(latencies))}ms" if latencies else "0ms"

        circuit = circuit_state.get(service.replace("-service", ""), {}).get("state", "CLOSED")

        print(f"| {service:<16} | {metrics[service]['status']:<6} | {avg_latency:<7} | {circuit:<8} | {metrics[service]['hits']:<11} |")

    print("+------------------+--------+---------+----------+-------------+")

    return {"message": "Health dashboard printed in console"}