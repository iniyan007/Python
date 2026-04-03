import asyncio
import json
import uuid
from datetime import datetime, timedelta

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import aiosqlite

app = FastAPI()

DB_NAME = "chat.db"


# ── DB helpers ────────────────────────────────────────────────────────────────

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            room      TEXT,
            sender    TEXT,
            receiver  TEXT,
            message   TEXT,
            timestamp TEXT
        )
        """)
        await db.commit()


async def save_message(room, sender, receiver, message):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO messages (room, sender, receiver, message, timestamp) VALUES (?, ?, ?, ?, ?)",
            (room, sender, receiver, message, datetime.now().strftime("%H:%M:%S"))
        )
        await db.commit()


async def get_history(room):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT sender, message, timestamp FROM messages WHERE room=? ORDER BY id ASC",
            (room,)
        )
        rows = await cursor.fetchall()
        # Return as list-of-dicts so JSON serialisation is clean
        return [{"sender": r[0], "message": r[1], "timestamp": r[2]} for r in rows]


async def search_messages(keyword):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT sender, message, timestamp FROM messages WHERE message LIKE ?",
            (f"%{keyword}%",)
        )
        rows = await cursor.fetchall()
        return [{"sender": r[0], "message": r[1], "timestamp": r[2]} for r in rows]



clients: dict[WebSocket, dict]  = {}   # ws -> {username, room}
rooms:   dict[str, set]         = {}   # room -> set of ws
user_sessions: dict[str, WebSocket] = {}  # username -> ws
last_seen: dict[str, datetime]  = {}   # username -> datetime of last activity


def log(msg: str):
    print(f"[INFO] {msg}")


# ── Broadcast helpers ─────────────────────────────────────────────────────────

async def broadcast(room: str, data: dict, exclude_ws: WebSocket | None = None):
    """Send data to every client in a room (optionally excluding one socket)."""
    for ws in list(rooms.get(room, [])):
        if ws is not exclude_ws:
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                pass


async def send_private(to_user: str, data: dict):
    ws = user_sessions.get(to_user)
    if ws:
        try:
            await ws.send_text(json.dumps(data))
        except Exception:
            pass


async def send_presence(room: str):
    """Broadcast the current presence list to everyone in the room."""
    now = datetime.now()
    users = []

    for ws in list(rooms.get(room, [])):
        info = clients.get(ws)
        if not info:
            continue
        u = info["username"]
        diff = now - last_seen.get(u, now)

        if diff < timedelta(seconds=10):
            status = "online"
        elif diff < timedelta(seconds=30):
            status = "away"
        else:
            status = "offline"

        users.append({"user": u, "status": status})

    await broadcast(room, {
        "type": "presence_list",
        "users": users,
        "count": len(users)
    })


# ── WebSocket endpoint ────────────────────────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    session_id = str(uuid.uuid4())[:6]
    username: str | None = None

    try:
        # First message must be {username: "..."}
        raw = await ws.receive_text()
        data = json.loads(raw)
        username = data.get("username", "").strip().lower()

        if not username:
            await ws.send_text(json.dumps({"type": "error", "message": "Username required"}))
            await ws.close()
            return

        clients[ws] = {"username": username, "room": None}
        user_sessions[username] = ws
        last_seen[username] = datetime.now()
        log(f'User "{username}" connected (session: {session_id})')

        # Confirm connection to client
        await ws.send_text(json.dumps({"type": "connected", "username": username}))

        # Main message loop
        while True:
            raw = await ws.receive_text()
            data = json.loads(raw)
            action = data.get("action")

            # Update last-seen for any activity
            last_seen[username] = datetime.now()

            # ── join ──────────────────────────────────────────────────────────
            if action == "join":
                old_room = clients[ws]["room"]

                # Leave old room
                if old_room and ws in rooms.get(old_room, set()):
                    rooms[old_room].discard(ws)
                    await broadcast(old_room, {
                        "type": "presence",
                        "message": f"{username} left {old_room}"
                    })
                    await send_presence(old_room)

                room = data.get("room", "").strip().lower()
                if not room:
                    continue

                clients[ws]["room"] = room
                rooms.setdefault(room, set()).add(ws)
                log(f"{username} joined room #{room}")

                # Send history to the joining user
                history = await get_history(room)
                await ws.send_text(json.dumps({"type": "history", "messages": history}))

                # Notify room and send presence list
                await broadcast(room, {
                    "type": "presence",
                    "message": f"{username} joined #{room}"
                }, exclude_ws=ws)
                await send_presence(room)

            # ── message ───────────────────────────────────────────────────────
            elif action == "message":
                room = clients[ws]["room"]
                if not room:
                    await ws.send_text(json.dumps({"type": "error", "message": "Join a room first"}))
                    continue

                msg = data.get("message", "").strip()
                if not msg:
                    continue

                ts = datetime.now().strftime("%H:%M:%S")
                await save_message(room, username, None, msg)

                payload = {
                    "type": "message",
                    "sender": username,
                    "message": msg,
                    "time": ts
                }
                await broadcast(room, payload, exclude_ws=ws)
                await ws.send_text(json.dumps(payload))
                log(f"[{room}] {username}: {msg}")

            # ── dm ────────────────────────────────────────────────────────────
            elif action == "dm":
                to_user = data.get("to", "").strip().lower()
                msg = data.get("message", "").strip()

                if not to_user or not msg:
                    continue

                if to_user not in user_sessions:
                    await ws.send_text(json.dumps({
                        "type": "error",
                        "message": f'User "{to_user}" is not online'
                    }))
                    continue

                ts = datetime.now().strftime("%H:%M:%S")
                await save_message(None, username, to_user, msg)

                payload = {
                    "type": "dm",
                    "from": username,
                    "to": to_user,
                    "message": msg,
                    "time": ts
                }

                await send_private(to_user, payload)
                await ws.send_text(json.dumps(payload))   # echo to sender
                log(f"[DM] {username} -> {to_user}: {msg}")

            # ── typing ────────────────────────────────────────────────────────
            elif action == "typing":
                room = clients[ws]["room"]
                if room:
                    await broadcast(room, {"type": "typing", "user": username}, exclude_ws=ws)

            # ── stop_typing ───────────────────────────────────────────────────
            elif action == "stop_typing":
                room = clients[ws]["room"]
                if room:
                    await broadcast(room, {"type": "stop_typing", "user": username}, exclude_ws=ws)

            # ── search ────────────────────────────────────────────────────────
            elif action == "search":
                keyword = data.get("keyword", "").strip()
                if keyword:
                    results = await search_messages(keyword)
                    await ws.send_text(json.dumps({"type": "search_results", "results": results, "keyword": keyword}))

            # ── ping (keep-alive / presence refresh) ──────────────────────────
            elif action == "ping":
                room = clients[ws]["room"]
                if room:
                    await send_presence(room)

    except WebSocketDisconnect:
        log(f'User "{username}" disconnected')

    except Exception as e:
        log(f"Error for {username}: {e}")

    finally:
        # Clean up
        if ws in clients:
            room = clients[ws]["room"]
            if room:
                rooms.get(room, set()).discard(ws)
            clients.pop(ws, None)

        if username:
            user_sessions.pop(username, None)
            last_seen.pop(username, None)

            room = None
            # Notify room of departure (find room from rooms dict)
            for r, ws_set in rooms.items():
                if not any(clients.get(w, {}).get("username") == username for w in ws_set):
                    room = r

            # Broadcast updated presence for all rooms this user was in
            for r in list(rooms.keys()):
                await send_presence(r)


# ── Startup ───────────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    await init_db()
    log("Chat server started on ws://0.0.0.0:8000/ws")


@app.get("/")
async def get():
    with open("client.html", "r") as f:
        return HTMLResponse(f.read())


if __name__ == "__main__":
    import uvicorn
    asyncio.run(init_db())
    log("Chat server started on ws://0.0.0.0:8000/ws")
    uvicorn.run(app, host="0.0.0.0", port=8000)