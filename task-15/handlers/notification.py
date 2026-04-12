import asyncio

async def notification_service(event):
    if event["type"] == "OrderPlaced":
        await asyncio.sleep(0.1)
        print(f"[HANDLER] Email sent to {event['customer']}")