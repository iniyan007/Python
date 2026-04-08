import asyncio
import random
from datetime import datetime

async def sensor_stream():
    while True:
        yield {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "sensor_id": "T1",
            "temperature": round(random.uniform(70, 110), 2),
            "vibration": round(random.uniform(0.1, 0.6), 2)
        }
        await asyncio.sleep(5)