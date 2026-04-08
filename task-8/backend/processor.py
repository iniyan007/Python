import pandas as pd

buffer = []
WINDOW = 300  # 5 min

def process(data):
    buffer.append(data)

    if len(buffer) > WINDOW:
        buffer.pop(0)

    df = pd.DataFrame(buffer)

    mean = df["temperature"].mean()
    std = df["temperature"].std()

    current = df.iloc[-1]["temperature"]
    z = (current - mean) / std if std != 0 else 0

    return {
        "avg": round(mean, 2),
        "z": round(z, 2),
        "current": current
    }