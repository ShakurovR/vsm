from fastapi import APIRouter, Path, Query
from schemas import VideoSearchResult, VideoSearchResultList
from services import search_list, search_one

router = APIRouter(prefix="/search", tags=["Поиск"])


@router.get(
    "/", response_model=list[VideoSearchResultList], description="Поиск списка видео"
)
def route_search_list(
    query: str = Query(max_length=250, description="Строка запроса"),
    video: int = Query(
        ge=0, le=100, description="Приоритет поиска по видео", default=90
    ),
    audio: int = Query(
        ge=0, le=100, description="Приоритет поиска по аудио", default=80
    ),
    text: int = Query(
        ge=0, le=100, description="Приоритет поиска по тексту", default=20
    ),
    hashtag: int = Query(
        ge=0, le=100, description="Приоритет поиска по хештегам", default=30
    ),
) -> list[VideoSearchResultList]:
    return search_list(
        query=query,
        video=video,
        audio=audio,
        text=text,
        hashtag=hashtag,
    )


@router.get(
    "/{id}",
    response_model=VideoSearchResult,
    description="Поиск элемента с подробным описанием результата поиска",
)
def route_search_item(
    query: str = Query(max_length=250, description="Строка запроса"),
    video: int = Query(
        ge=0, le=100, description="Приоритет поиска по видео", default=90
    ),
    audio: int = Query(
        ge=0, le=100, description="Приоритет поиска по аудио", default=80
    ),
    text: int = Query(
        ge=0, le=100, description="Приоритет поиска по тексту", default=20
    ),
    hashtag: int = Query(
        ge=0, le=100, description="Приоритет поиска по хештегам", default=30
    ),
    id: int = Path(description="Идентификатор видео"),
) -> VideoSearchResult:
    return search_one(
        id=id, query=query, video=video, audio=audio, text=text, hashtag=hashtag
    )
