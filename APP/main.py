from fastapi import FastAPI

app = FastAPI(title="My API")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}