import os

from chromadb import HttpClient
from core.database import get_db
from core.settings import get_settings
from fastapi import HTTPException, status
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from schemas import (
    VideoRead,
    VideoSearchResult,
    VideoSearchResultList,
    VideoSearchResultReason,
)
from services.pipelineutils import translation

from .video import get_one as get_video

SETTINGS = get_settings()

CHROMA_EMB = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    model_kwargs={"trust_remote_code": True},
)

chromaclient = HttpClient(host=os.getenv("CHROMA_HOST", "chroma"))
CHClient = Chroma(
    persist_directory="video",
    embedding_function=CHROMA_EMB,
    collection_metadata={"hnsw:space": "cosine"},
    client=chromaclient,
)


def get_correction_scope(correction: dict, data: tuple[Document, float]) -> float:
    video_id = data[0].metadata.get("video_id")
    type_data = data[0].metadata.get("type_data")
    return (video_id, correction[type_data] * data[1])


def get_videos_scope(datum: list[tuple[int, float]]) -> list[VideoSearchResultList]:
    scores = {}
    for data in datum:
        if scores.get(data[0]) is None:
            scores[data[0]] = [data[1]]
        else:
            scores[data[0]].append(data[1])
    db = get_db().__next__()
    result = []
    for video_id in scores:
        video = VideoRead.model_validate(get_video(db=db, id=video_id))
        result.append(
            VideoSearchResultList(
                id=video_id,
                name=video.name,
                length=video.length,
                description=video.description,
                checksum=video.checksum,
                preview=video.urls.get("preview"),
                score=max(scores[video_id]),
                video=video.urls.get("video"),
            )
        )
    result = sorted(result, key=lambda x: x.score, reverse=True)
    return result


def filter_docs(
    id: int, datum: list[tuple[Document, float]], correction: dict
) -> VideoSearchResult:

    results = [data for data in datum if data[0].metadata.get("video_id") == id]
    if len(results) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )
    db = get_db().__next__()
    video = get_video(db=db, id=id)
    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )
    video = VideoRead.model_validate(video)
    reasons = []
    scores = []
    for result in results:
        if result[0].metadata.get("type_data") == "video":
            url = f"{SETTINGS.api_media_url}{video.checksum}/frames/{int(float(result[0].metadata.get('time')))}.png"
        else:
            url = None
        reasons.append(
            VideoSearchResultReason(
                type_data=result[0].metadata.get("type_data"),
                content=result[0].page_content,
                url=url,
                score=result[1] * correction[result[0].metadata.get("type_data")],
            )
        )
        scores.append(result[1] * correction[result[0].metadata.get("type_data")])
    reasons = sorted(reasons, key=lambda x: x.score, reverse=True)
    return VideoSearchResult(
        name=video.name,
        description=video.description,
        length=video.length,
        checksum=video.checksum,
        score=max(scores),
        reasons=reasons,
    )


def search_list(
    query: str, video: int, audio: int, text: int, hashtag: int
) -> list[VideoSearchResultList]:
    correction = {
        "video": video / 100,
        "audio": audio / 100,
        "text": text / 100,
        "hashtag": hashtag / 100,
    }

    en_query = translation(query)
    docs = CHClient.similarity_search_with_relevance_scores(query=en_query, k=10)
    ids_score = list(
        map(lambda doc: get_correction_scope(correction=correction, data=doc), docs)
    )

    result = get_videos_scope(datum=ids_score)

    return result


def search_one(
    id: int, query: str, video: int, audio: int, text: int, hashtag: int
) -> VideoSearchResult:
    correction = {
        "video": video / 100,
        "audio": audio / 100,
        "text": text / 100,
        "hashtag": hashtag / 100,
    }

    en_query = translation(query)
    docs = CHClient.similarity_search_with_relevance_scores(query=en_query, k=10)
    return filter_docs(id=id, datum=docs, correction=correction)
