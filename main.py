import time, asyncio
from fastapi import FastAPI

app = FastAPI()


@app.get("/sync-call")
def sync_call():
    time.sleep(3)  # simulates blocking I/O (e.g., slow API call)
    return {"message": "Finished sync call"}


@app.get("/async-call")
async def async_call():
    await asyncio.sleep(3)  # simulates non-blocking I/O
    return {"message": "Finished async call"}
