from core.database import Base
from core.schema import SuccessResult
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def generate_services(
    db_model: Base,
    create_schema,
    read_schema,
    read_list_schema,
    update_schema,
):
    def get_one(db: Session, id: int) -> read_schema:
        try:
            result = db.query(db_model).filter(db_model.id == id).first()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
            )
        return result

    def get_all(
        db: Session, offset: int = 0, limit: int | None = None
    ) -> list[read_list_schema]:
        try:
            result = db.query(db_model).offset(offset).limit(limit).all()
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
            )
        return result

    def create(db: Session, create: create_schema) -> read_schema:
        try:
            db_instance = db_model(**create.model_dump())
            db.add(db_instance)
            db.commit()
            db.refresh(db_instance)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
            )
        return db_instance

    def count(db: Session) -> int:
        try:
            result = db.query(db_model.id).count()
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
            )
        return result

    def update(db: Session, id: int, update: update_schema) -> read_schema:
        try:
            db_instance: db_model = get_one(db=db, id=id)
            if not db_instance:
                raise HTTPException(status_code=404, detail="Record not found")
            update_data = update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_instance, key, value)
            db.add(db_instance)
            db.commit()
            db.refresh(db_instance)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
            )
        return db_instance

    def find_one(db: Session, default: dict) -> read_schema:
        try:
            statements = list()
            for key in list(default.keys()):
                statements.append(getattr(db_model, key) == default.get(key, None))
            result = db.query(db_model).where(*statements)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
            )
        return result.first()

    def find_all(db: Session, default: dict) -> list[read_list_schema]:
        try:
            statements = list()
            for key in list(default.keys()):
                statements.append(getattr(db_model, key) == default.get(key, None))
            result = db.query(db_model).where(*statements)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
            )
        return result.all()

    def delete(db: Session, id: int) -> SuccessResult:
        try:
            db_instance = get_one(db=db, id=id)
            if not db_instance:
                raise HTTPException(status_code=404, detail="Record not found")
            db.delete(db_instance)
            db.commit()
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
            )
        return SuccessResult(success=True)

    return (create, get_one, get_all, find_one, find_all, update, delete, count)
