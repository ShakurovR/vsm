from pydantic import BaseModel


class SuccessResult(BaseModel):
    success: bool


class Pagination(BaseModel):
    offset: int = 0
    limit: int | None = None


class TaskStatus(BaseModel):
    status: str


class TaskResult(BaseModel):
    task_id: str
