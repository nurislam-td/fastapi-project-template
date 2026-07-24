import uvicorn
from diwire.integrations.fastapi import RequestContextMiddleware, add_request_context
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from setup.api import router as api_router
from setup.di.ioc import container
from shared.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1",
    docs_url=settings.DOCS_URL,
    openapi_url=settings.OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)

app.add_middleware(RequestContextMiddleware)
add_request_context(container)


@app.get("/")
async def health_check() -> dict[str, str]:
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
    )
