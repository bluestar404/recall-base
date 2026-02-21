from fastapi import FastAPI

app = FastAPI(title="Recall Base - AI Memory Backend")


@app.get("/health")
def health_check():
    return {"status": "ok"}