import os

import pandas as pd
from celery import shared_task
from celery_apps import indexer_task, uploader_celery
from core.database import get_db
from models import Video
from services.upload import _upload_file


@shared_task(name="uploader.csv", bind=True)
def start(self, csvfilepath: str) -> None:
    uploader_celery
    df = pd.read_csv(csvfilepath)
    df = df.where(pd.notnull(df), None)
    ddf = df.to_dict("records")
    percent = 0
    csv_count = len(ddf)
    db = get_db().__next__()
    checksums = db.query(Video.checksum).all()
    db.close()
    checksums = [cs[0] for cs in checksums]
    self.update_state(
        task_id=self.request.id,
        state="PROGRESS",
        meta={"status": str(percent)},
    )
    for i, row in enumerate(ddf):
        db = get_db().__next__()
        print(f"Num: {i}, count {csv_count}")
        if int(i / csv_count * 100) != percent:
            percent = int(i / csv_count * 100)
            print(f"{percent}% ready")
            self.update_state(
                task_id=self.request.id,
                state="PROGRESS",
                meta={"status": str(percent)},
            )
        url = row.get("link")
        if url is None:
            continue
        description = row.get("description")
        print(f"Start uploading from {url}")
        filepath, checksum = _upload_file(url=url)
        if checksum in checksums:
            continue

        print("Get preview and length")
        task_id, preview = indexer_task(
            "indexer.get_preview", filepath=filepath, wait_result=True
        )
        task_id, length = indexer_task(
            "indexer.get_length", filepath=filepath, wait_result=True
        )

        video = Video(
            name=url.split("/")[-1],
            length=length,
            checksum=checksum,
            description=description,
            original_url=url,
        )
        db.add(video)
        db.commit()
        db.refresh(video)
        if not video.is_indexed:
            task, _ = indexer_task("indexer.file", filepath=filepath, video_id=video.id)
            print(f"Send task {task}")
            video.current_task = task
            db.add(video)
            db.commit()
        db.close()
    os.remove(csvfilepath)
