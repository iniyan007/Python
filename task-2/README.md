# 💬 Real-Time Chat Application with WebSockets

## 📌 Overview

This project is a **real-time multi-room chat application** built using **FastAPI WebSockets** and a modern HTML/JS frontend.

It supports:

- Multi-room chat
- Direct messaging (DM)
- Typing indicators
- User presence tracking (online/away/offline)
- Message persistence with SQLite
- Message search functionality

---

## 🚀 Features

### 🧑‍🤝‍🧑 Chat Rooms

- Users can join named rooms dynamically
- Each room maintains its own message stream

### 💌 Private Messaging (DM)

- Send messages directly to a specific user
- Works only if the user is online

### ⌨️ Typing Indicators

- Shows "user is typing..." in real-time
- Automatically clears after inactivity

### 🟢 Presence Tracking

- Displays:
  - 🟢 Online (<10 sec activity)
  - 🟡 Away (<30 sec inactivity)
  - ⚪ Offline (>30 sec inactivity)

### 💾 Message Persistence

- Messages stored in SQLite (`chat.db`)
- History loaded when user joins room

### 🔍 Search Messages

- Keyword-based message search across database

---

## 🛠️ Tech Stack

### Backend

- **FastAPI** – Web framework
- **WebSockets** – Real-time communication
- **aiosqlite** – Async database operations
- **asyncio** – Concurrency

### Frontend

- HTML, CSS, JavaScript
- Native WebSocket API

---

## ⚙️ How It Works

### 1. WebSocket Connection

- Client connects to:

```

ws://localhost:8000/ws

````

- First message must include username:

```json
{ "username": "john" }
````

---

### 2. Room Management

#### Join Room

```json
{
  "action": "join",
  "room": "general"
}
```

* Loads message history
* Broadcasts presence updates

---

### 3. Messaging System

#### Send Message

```json
{
  "action": "message",
  "message": "Hello everyone!"
}
```

* Broadcast to room
* Stored in database

---

### 4. Direct Messaging (DM)

```json
{
  "action": "dm",
  "to": "alice",
  "message": "Hey!"
}
```

* Sent privately
* Stored separately

---

### 5. Typing Indicators

```json
{ "action": "typing" }
{ "action": "stop_typing" }
```

---

### 6. Presence System

* Uses `last_seen` timestamps
* Automatically updates:

  * Online
  * Away
  * Offline

---

### 7. Search Messages

```json
{
  "action": "search",
  "keyword": "error"
}
```

* Returns matching messages from DB

---

## 🗄️ Database Schema

```sql
CREATE TABLE messages (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    room      TEXT,
    sender    TEXT,
    receiver  TEXT,
    message   TEXT,
    timestamp TEXT
);
```

---

## ▶️ Running the Application

### 1. Install Dependencies

```bash
pip install fastapi uvicorn aiosqlite
```

---

### 2. Run Server

```bash
python main.py
```

Server runs at:

```
http://localhost:8000
```

---

### 3. Open Client

* Open browser:

```
http://localhost:8000
```

---

## 🧪 Sample Flow

1. Enter username
2. Join a room (e.g., `general`)
3. Start chatting
4. Send DMs
5. Search messages
6. See live presence updates

---

## 📡 WebSocket Event Types

| Type           | Description             |
| -------------- | ----------------------- |
| connected      | User connected          |
| message        | Room message            |
| dm             | Private message         |
| typing         | User typing             |
| stop_typing    | Typing stopped          |
| presence       | Join/leave notification |
| presence_list  | Active users list       |
| history        | Previous messages       |
| search_results | Search output           |
| error          | Error message           |

---

## ⚡ Key Concepts Used

* WebSocket protocol (full-duplex communication)
* Async programming (`async/await`)
* JSON message passing
* State management (rooms, users, sessions)
* Real-time UI updates

---

## 📌 Use Cases

* Team collaboration tools
* Live customer support chat
* Gaming chat systems
* Classroom discussion platforms
