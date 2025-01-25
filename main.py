import signal
from fastapi import FastAPI
from utils.init_db import create_tables
from routers.api import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    debug=True,
    title="Online Learning API",
)

running = True

def stop_server(*args):
    global running
    running = False

@app.on_event("startup")
def on_startup() -> None:
    """
    Initializes the database tables when the application starts up.
    """
    create_tables()
    signal.signal(signal.SIGINT, stop_server)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)