import signal
from fastapi import FastAPI
from utils.init_db import create_tables
from routers.api import router

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


app.include_router(router)



