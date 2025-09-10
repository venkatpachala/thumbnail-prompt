from __future__ import annotations

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routes import background, cutout, compose
from .utils import paths

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="thumbnail-generator")

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

paths.ensure_dirs()
app.mount("/files", StaticFiles(directory=paths.storage_root()), name="files")

app.include_router(background.router)
app.include_router(cutout.router)
app.include_router(compose.router)


@app.get("/health")
async def health():
    return {"ok": True}
