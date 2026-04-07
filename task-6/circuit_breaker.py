import time
from config import CIRCUIT_BREAKER

circuit_state = {}

def get_state(service):
    return circuit_state.get(service, {
        "failures": 0,
        "state": "CLOSED",
        "last_failed": 0
    })

def record_failure(service):
    state = get_state(service)
    state["failures"] += 1
    state["last_failed"] = time.time()

    if state["failures"] >= CIRCUIT_BREAKER["FAIL_THRESHOLD"]:
        state["state"] = "OPEN"

    circuit_state[service] = state


def record_success(service):
    circuit_state[service] = {
        "failures": 0,
        "state": "CLOSED",
        "last_failed": 0
    }


def is_open(service):
    state = get_state(service)

    if state["state"] == "OPEN":
        if time.time() - state["last_failed"] > CIRCUIT_BREAKER["RECOVERY_TIME"]:
            state["state"] = "HALF_OPEN"
            circuit_state[service] = state
            return False
        return True

    return False