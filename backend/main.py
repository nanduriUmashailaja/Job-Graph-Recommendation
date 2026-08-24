from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Job Graph Recommender is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }