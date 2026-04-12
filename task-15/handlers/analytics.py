analytics_db = {"revenue": 0}

async def analytics_projection(event):
    if event["type"] == "OrderPlaced":
        analytics_db["revenue"] += event["total"]
        print(f"[HANDLER] Revenue updated: {analytics_db['revenue']}")