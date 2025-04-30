from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from server import routers
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings
from pathlib import Path
import os
import json
from config import config
from helpers import Database

app = FastAPI()

app.mount(
    f"/{config.static_dir}", StaticFiles(directory=config.static_dir), config.static_dir
)

for router in routers:
    app.include_router(router)


databases = Database()

print(databases)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return databases.render(request)


@app.get("/api/databases")
async def get_databases():
    print(list(map(databases.values(), lambda x: x.model_dump())))
    return


@app.get("/api/databases/{id}")
async def get_database(id: int):
    return databases.get(id)


@app.patch("/api/databases/{id}")
async def update_database_status(id: int, update: dict):
    status = update.get("status")
    if status is None:
        raise HTTPException(status_code=400, detail="status is required")
    return databases.update(id, status=status).save()


@app.put("/api/databases/{id}")
async def update_database(id: int, update: dict):
    return databases.update(id, **update).save()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
