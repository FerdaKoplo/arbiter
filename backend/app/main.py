from fastapi import FastAPI

app = FastAPI(title="Arbiter")


@app.get("/health")
def health():
    return {"status": "ok"}
