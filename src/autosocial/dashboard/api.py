from fastapi import FastAPI
from autosocial.queue.manager import QueueManager

app = FastAPI(title="AutoSocial AI Dashboard API")

# Simple dependency injection pattern for queue (stub)
queue = QueueManager()

@app.get("/")
async def root():
    return {"status": "ok", "app": "AutoSocial AI"}

@app.get("/queue/pending")
async def get_pending():
    return {"pending": queue.get_pending()}

@app.get("/queue/ready")
async def get_ready():
    return {"ready": queue.get_ready()}

@app.post("/trigger/research")
async def trigger_research():
    return {"status": "triggered", "message": "Research pipeline started"}
