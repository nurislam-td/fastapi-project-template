import uvicorn
from diwire.integrations.fastapi import RequestContextMiddleware, add_request_context
from fastapi import FastAPI

from setup.api import router as api_router
from setup.di.ioc import container
from shared.settings import get_settings

settings = get_settings()

app = FastAPI()
app.include_router(api_router)

app.add_middleware(RequestContextMiddleware)
add_request_context(container)


@app.get("/")
async def health_check():
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
    )
