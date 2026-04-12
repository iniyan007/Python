from collections import defaultdict

class EventStore:
    def __init__(self):
        self.store = defaultdict(list)

    def append(self, aggregate_id, events):
        for event in events:
            self.store[aggregate_id].append(event)
        print(f"[EVENT STORE] Appended {len(events)} events")

    def get_events(self, aggregate_id):
        return self.store[aggregate_id]

    def replay(self, aggregate_id):
        events = self.get_events(aggregate_id)

        state = {
            "id": aggregate_id,
            "status": None,
            "total": 0,
            "items": 0
        }

        for event in events:
            if event["type"] == "OrderPlaced":
                state["status"] = "PLACED"
                state["total"] = event["total"]
                state["items"] = event["items"]

            elif event["type"] == "OrderUpdated":
                state["total"] = event["new_total"]
                state["items"] -= 1

            elif event["type"] == "PaymentProcessed":
                state["status"] = "PAID"

            elif event["type"] == "OrderShipped":
                state["status"] = "SHIPPED"

        return state