from fastapi import FastAPI
app = FastAPI()

@app.get("/products/{id}")
def product(id: int):
    return {"id": id, "name": "Product"}