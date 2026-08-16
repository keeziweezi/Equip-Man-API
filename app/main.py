from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return{"message": "Equipment Management API is running"}

@app.get("/equipment")
def list_equipment():
    return {"equipment": []}

@app.post("/equipment")
def create_equipment(name: str, category: str):
    return {"name": name, "category": category}