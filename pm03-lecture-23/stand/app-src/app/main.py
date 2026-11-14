import os
from fastapi import FastAPI
from sqlalchemy import create_engine, text

VERSION = "1.4.0"
app = FastAPI(title="Cloud Application", version=VERSION)
engine = create_engine(os.environ["DATABASE_URL"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"version": VERSION, "environment": os.environ.get("APP_ENV", "unknown")}

@app.get("/items")
def items():
    with engine.connect() as c:
        rows = c.execute(text("select id, name, priority from items order by id")).all()
    return [{"id": r.id, "name": r.name, "priority": r.priority} for r in rows]
