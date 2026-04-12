import uuid
from datetime import datetime

class OrderAggregate:
    def __init__(self):
        self.events = []

    def place_order(self, command):
        order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        total = sum(i["qty"] * i["price"] for i in command.items)

        event = {
            "type": "OrderPlaced",
            "order_id": order_id,
            "customer": command.customer_id,
            "total": total,
            "items": sum(i["qty"] for i in command.items),
            "timestamp": datetime.utcnow().isoformat()
        }

        self.events.append(event)

        for item in command.items:
            self.events.append({
                "type": "InventoryReserved",
                "sku": item["sku"],
                "qty": item["qty"]
            })

        print(f"[WRITE] Order {order_id} created")
        return order_id, self.events

    def update_order(self, order_id, removed_price):
        event = {
            "type": "OrderUpdated",
            "order_id": order_id,
            "new_total": removed_price,
            "timestamp": datetime.utcnow().isoformat()
        }
        return [event]

    def process_payment(self, order_id, amount):
        return [{
            "type": "PaymentProcessed",
            "order_id": order_id,
            "amount": amount,
            "method": "card_ending_4242",
            "timestamp": datetime.utcnow().isoformat()
        }]

    def ship_order(self, order_id):
        return [{
            "type": "OrderShipped",
            "order_id": order_id,
            "tracking": "1Z999AA10123456784",
            "timestamp": datetime.utcnow().isoformat()
        }]