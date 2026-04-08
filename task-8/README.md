# 📄 📘 REAL-TIME DATA STREAMING DASHBOARD (DOCUMENTATION)

---

## 🚀 Project Overview

This project implements a **real-time data streaming dashboard** that:

* Simulates IoT sensor data (temperature & vibration)
* Processes data using **windowed aggregation**
* Detects anomalies using **Z-score**
* Streams live updates via **WebSockets**
* Displays data in a **browser dashboard**
* Sends **email alerts** on critical conditions

---

## 🧠 System Architecture

```text
Sensor Simulation (Async)
        ↓
Data Processing (pandas)
        ↓
Anomaly Detection (Z-score)
        ↓
WebSocket Server (FastAPI)
        ↓
Frontend Dashboard (Chart.js)
        ↓
Email Alert System
```

---

## ⚙️ Tech Stack

### Backend

* Python
* FastAPI (WebSockets)
* asyncio
* pandas
* smtplib (email)

### Frontend

* HTML, CSS, JavaScript
* Chart.js

---

## 🔄 Workflow

1. Sensor data is generated every 5 seconds
2. Data is stored in a rolling buffer (5-minute window)
3. Moving average and Z-score are calculated
4. If anomaly detected:

   * Status set to **CRITICAL**
   * Email alert triggered
5. Data is sent to frontend via WebSocket
6. Dashboard updates in real time

---

## 🧪 Backend Implementation

### 🔹 WebSocket Server

* Accepts client connections
* Streams processed data every 5 seconds
* Sends JSON payload

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
```

---

### 🔹 Data Processing

* Maintains rolling buffer
* Computes:

  * Moving Average
  * Standard Deviation
  * Z-score

```python
z = (current - mean) / std if std != 0 else 0
```

---

### 🔹 Anomaly Detection

```python
status = "CRITICAL" if abs(z) > 2 else "OK"
```

---

### 🔹 Email Alert

* Triggered when status = CRITICAL
* Uses SMTP (Gmail)

```python
send_email_alert(sensor_id, current, avg, z_score)
```

---

## 🌐 Frontend Implementation

Your frontend UI (from your uploaded file ) includes:

### ✅ Features

* 📈 Live updating line chart
* 📊 Metrics panel:

  * Current temperature
  * Moving average
  * Z-score
  * Alert count
* 🟢 WebSocket status indicator
* 🚨 Alert log panel
* 🎨 Dynamic UI (color + animations)

---

### 🔹 WebSocket Connection

```javascript
const ws = new WebSocket('ws://127.0.0.1:8000/ws');
```

---

### 🔹 Real-Time Chart Update

```javascript
chart.data.labels.push(data.timestamp);
chart.data.datasets[0].data.push(data.current);
chart.update('none');
```

---

### 🔹 Alert Handling

```javascript
if (data.status === 'CRITICAL') {
    addAlert(data);
}
```

---

## 📊 Sample Output

### 🖥 Backend Console

```text
[11:37:51] OK | Temp: 90.63°F | Avg: 90.63°F | Z-score: nan
[11:38:06] OK | Temp: 109.57°F | Avg: 96.88°F | Z-score: 1.42
```

---

### 🌐 Dashboard

* Live graph updates
* Alerts displayed with timestamps
* Metrics update instantly

---

## 🚨 Alert System

### Trigger Condition

```text
| Z-score | > 2
```

---

### Email Example

```txt
ALERT TRIGGERED!

Sensor: T1
Current Temp: 104.2°F
Moving Avg: 82.4°F
Z-Score: 2.7

Action Required!
```

---

## ▶️ How to Run

### 1️⃣ Start Backend

```bash
cd backend
uvicorn main:app --host 127.0.0.1 --port 8000
```

---

### 2️⃣ Start Frontend

```bash
cd frontend
python -m http.server 5500
```

Open:

```txt
http://localhost:5500
```

---

## 🧪 Testing

| Scenario       | Expected Result          |
| -------------- | ------------------------ |
| Normal data    | Status = OK              |
| High deviation | Status = CRITICAL        |
| Critical       | Email sent + alert shown |

---

## 🔥 Key Features

* ✅ Real-time data streaming
* ✅ Async architecture
* ✅ WebSocket communication
* ✅ Rolling window analytics
* ✅ Anomaly detection (Z-score)
* ✅ Email alert system
* ✅ Interactive dashboard UI
