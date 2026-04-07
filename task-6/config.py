ROUTES = {
    "users": "http://localhost:3001",
    "orders": "http://localhost:3002",
    "products": "http://localhost:3003"
}

RATE_LIMIT = 5  # req/min
WINDOW = 60      # seconds

CACHE_TTL = 60   # seconds

CIRCUIT_BREAKER = {
    "FAIL_THRESHOLD": 5,
    "RECOVERY_TIME": 30
}