# main.py
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from processor import process
from alert import send_email_alert

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("\n[WS] ✓ Client connected")
    print("-" * 50)

    try:
        while True:
            raw = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "sensor_id": "T1",
                "temperature": round(random.uniform(70, 110), 2),
                "vibration": round(random.uniform(0.1, 0.6), 2),
            }

            result = process(raw)
            status = "CRITICAL" if abs(result["z"]) > 2 else "OK"

            payload = {
                "timestamp": raw["timestamp"],
                "sensor_id": raw["sensor_id"],
                "current": result["current"],
                "avg": result["avg"],
                "z_score": result["z"],
                "status": status,
            }
            indicator = "🚨 CRITICAL" if status == "CRITICAL" else "✅ OK      "
            print(
                f"[{raw['timestamp']}] {indicator} | "
                f"Temp: {result['current']}°F | "
                f"Avg: {result['avg']}°F | "
                f"Z-score: {result['z']}"
            )
            await websocket.send_text(json.dumps(payload))
            if status == "CRITICAL":
                print(f"  └─ Sending email alert for sensor {raw['sensor_id']}...")
                await asyncio.to_thread(
                    send_email_alert,
                    raw["sensor_id"],
                    result["current"],
                    result["avg"],
                    result["z"]
                )
                print(f"  └─ Email sent.")

            await asyncio.sleep(5)

    except (WebSocketDisconnect, ConnectionClosedOK, ConnectionClosedError):
        print("\n[WS] Client disconnected\n")

    except Exception as e:
        print(f"\n[WS ERROR] {e}\n")