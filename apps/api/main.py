import uvicorn
from core.database import init_db
from core.logging import LOG_FORMAT
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import router_index, router_search, router_upload, router_video

app = FastAPI(
    description="API сервис по содержимому в контенте сервиса Yappy: видео, аудио, текст",
    title="Yappy Media Search API",
    summary="Разработан в рамках хакатона ЛЦТ-2024 командой Простите у нас вдохновение",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()


app.include_router(router_search)
app.include_router(router_index)
app.include_router(router_upload)
app.include_router(router_video)


@app.get("/healthcheck", tags=["Healthcheck"])
def healthcheck():
    return JSONResponse(status_code=200, content={"healthchek": True})


if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = LOG_FORMAT
    log_config["formatters"]["default"]["fmt"] = LOG_FORMAT
    uvicorn.run(
        "main:app", host="0.0.0.0", port=9000, reload=True, log_config=log_config
    )
