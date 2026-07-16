import uvicorn
from fastapi import FastAPI

from shared.settings import get_settings

settings = get_settings()

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
    )
