import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import Scope, Receive, Send

from backend.database import supabase, get_db
from backend.routers import listings, areas, contact, auth, favorites


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Keja Go", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listings.router)
app.include_router(areas.router)
app.include_router(contact.router)
app.include_router(auth.router)
app.include_router(favorites.router)


@app.get("/api/health")
async def health():
    try:
        await supabase.select("listings", limit=1)
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)[:200]}


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
os.makedirs(str(FRONTEND_DIR), exist_ok=True)

if FRONTEND_DIR.exists():

    class NoCacheStaticFiles(StaticFiles):
        async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
            original_send = send
            async def send_with_headers(message):
                if message["type"] == "http.response.start":
                    headers = message.get("headers", [])
                    cache_headers = [
                        (b"cache-control", b"no-cache, no-store, must-revalidate"),
                        (b"pragma", b"no-cache"),
                        (b"expires", b"0"),
                    ]
                    existing = dict(headers)
                    existing.update(dict(cache_headers))
                    message["headers"] = list(existing.items())
                await original_send(message)
            await super().__call__(scope, receive, send_with_headers)

    app.mount(
        "/",
        NoCacheStaticFiles(directory=str(FRONTEND_DIR), html=True),
        name="frontend",
    )
