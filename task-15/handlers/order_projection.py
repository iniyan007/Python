from read_model.read_store import read_store

async def order_dashboard_projection(event):
    order = read_store.get_order(event.get("order_id"))

    if event["type"] == "OrderPlaced":
        read_store.insert_order({
            "order_id": event["order_id"],
            "customer_id": event["customer"],
            "status": "PLACED",
            "total": event["total"],
            "item_count": event["items"],
            "placed_at": event["timestamp"]
        })

    elif event["type"] == "OrderUpdated" and order:
        order["total"] = event["new_total"]
        order["item_count"] -= 1

    elif event["type"] == "PaymentProcessed" and order:
        order["status"] = "PAID"

    elif event["type"] == "OrderShipped" and order:
        order["status"] = "SHIPPED"