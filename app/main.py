from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from uuid import uuid4

app = FastAPI(title="RecallBase", version="0.1.0")

memories = {}  #temporary memory storage

class MemoryCreate(BaseModel):
    content:str
    tags:list[str]=[]

@app.get("/health")
def health():
    return {"status": "ok", "message": "RecallBase is running"}

@app.post("/memories", status_code=201)
def add_memory(body: MemoryCreate):
    mem_id = str(uuid4())
    memories[mem_id] = {
        "id":mem_id,
        "content": body.content,
        "tags":body.tags,
        "created_at": datetime.now(timezone.utc).isoformat() 
    }
    return memories[mem_id]

@app.get("/memories")
def get_all_memories():
    return list(memories.values())

@app.get("/memories/{memory_id}")
def get_memory(memory_id:str):
    if memory_id not in memories:
        raise HTTPException(status_code =404, detail="Memory not found")
    return memories[memory_id]

@app.delete("/memories/{memory_id}", status_code=204)
def delete_memory(memory_id: str):
    if memory_id not in memories:
        raise HTTPException(status_code = 404, detail = "Memory not found")
    del memories[memory_id]