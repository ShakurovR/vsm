from core.exception import NotFound
from core.schema import Pagination, SuccessResult
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


def generate_router(
    get_db,
    create_schema,
    read_schema,
    read_list_schema,
    update_schema,
    func_create=None,
    func_get_one=None,
    func_get_all=None,
    func_update=None,
    func_delete=None,
    func_count=None,
    prefix: str = "",
    tags: list = [],
    user_depend=None,
):
    router = APIRouter(prefix=prefix, tags=tags)

    if func_create:

        @router.post("/", response_model=read_schema)
        def route_create(
            create: create_schema,
            db: Session = Depends(get_db),
        ) -> read_schema:
            return func_create(db=db, create=create)

    if func_get_all:

        @router.get("/", response_model=list[read_list_schema])
        def route_get_all(
            db: Session = Depends(get_db),
            pagination: Pagination = Depends(Pagination),
        ) -> list[read_list_schema]:
            return func_get_all(db=db, offset=pagination.offset, limit=pagination.limit)

    if func_get_one:

        @router.get("/{id}", response_model=read_schema)
        def route_get_one(
            id: int,
            db: Session = Depends(get_db),
        ) -> read_schema:
            result = func_get_one(db=db, id=id)
            if result is None:
                raise NotFound()
            return result

    if func_count:

        @router.get("/count/", response_model=int)
        def route_count(
            db: Session = Depends(get_db),
        ) -> int:
            return func_count(db=db)

    if func_update:

        @router.patch("/{id}", response_model=read_schema)
        def route_update(
            id: int,
            update: update_schema,
            db: Session = Depends(get_db),
        ) -> read_schema:
            return func_update(db=db, id=id, update=update)

    if func_delete:

        @router.delete("/{id}", response_model=SuccessResult)
        def route_delete(
            id: int,
            db: Session = Depends(get_db),
        ) -> SuccessResult:
            return func_delete(db=db, id=id)

    return router
