from fastapi import FastAPI
app = FastAPI()

@app.get("/users")
def get_users():
    return {"users": ["Alice", "Bob"]}