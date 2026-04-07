from fastapi import FastAPI
app = FastAPI()

@app.get("/orders/latest")
def latest():
    return {"order": "latest"}